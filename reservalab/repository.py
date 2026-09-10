"""Persistência SQLite; uma conexão por operação e escrita serializada."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from uuid import uuid4

from .domain import DomainError


class BookingRepository:
    """Mantém salas e reservas sem compartilhar conexões entre threads."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        if self.db_path == ":memory:":
            raise ValueError("Use um arquivo SQLite; bancos :memory: não são suportados.")
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    capacity INTEGER NOT NULL CHECK (capacity > 0)
                );
                CREATE TABLE IF NOT EXISTS bookings (
                    id TEXT PRIMARY KEY,
                    room_id INTEGER NOT NULL REFERENCES rooms(id),
                    student_name TEXT NOT NULL,
                    starts_at TEXT NOT NULL,
                    ends_at TEXT NOT NULL,
                    participants INTEGER NOT NULL CHECK (participants > 0),
                    status TEXT NOT NULL CHECK (status IN ('active', 'cancelled'))
                );
                CREATE INDEX IF NOT EXISTS bookings_room_interval
                    ON bookings(room_id, status, starts_at, ends_at);
                INSERT OR IGNORE INTO rooms (id, name, capacity) VALUES (1, 'Sala 1', 4);
                INSERT OR IGNORE INTO rooms (id, name, capacity) VALUES (2, 'Sala 2', 8);
                """
            )

    @contextmanager
    def _connection(self):
        connection = sqlite3.connect(self.db_path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def list_rooms(self) -> list[dict]:
        with self._connection() as connection:
            return [dict(row) for row in connection.execute("SELECT id, name, capacity FROM rooms ORDER BY id")]

    def list_bookings(self) -> list[dict]:
        with self._connection() as connection:
            return [dict(row) for row in connection.execute("SELECT * FROM bookings ORDER BY starts_at, id")]

    def create_booking(self, booking: dict) -> dict:
        """Valida conflito e insere na mesma transação, inclusive sob concorrência."""
        if booking["room_id"] > 2**63 - 1:
            raise DomainError("room_not_found", "Sala não encontrada.", 404)
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            room = connection.execute("SELECT capacity FROM rooms WHERE id = ?", (booking["room_id"],)).fetchone()
            if room is None:
                raise DomainError("room_not_found", "Sala não encontrada.", 404)
            if booking["participants"] > room["capacity"]:
                raise DomainError("invalid_participants", "O número de participantes excede a capacidade da sala.")
            conflict = connection.execute(
                """SELECT 1 FROM bookings
                   WHERE room_id = ? AND status = 'active'
                     AND starts_at < ? AND ends_at > ? LIMIT 1""",
                (booking["room_id"], booking["ends_at"], booking["starts_at"]),
            ).fetchone()
            if conflict is not None:
                raise DomainError("booking_conflict", "A sala já está reservada nesse intervalo.", 409)
            result = {"id": str(uuid4()), **booking, "status": "active"}
            connection.execute(
                """INSERT INTO bookings
                   (id, room_id, student_name, starts_at, ends_at, participants, status)
                   VALUES (:id, :room_id, :student_name, :starts_at, :ends_at, :participants, :status)""",
                result,
            )
            return result

    def cancel_booking(self, booking_id: str) -> dict:
        """Cancelar novamente mantém o resultado e não remove o histórico."""
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
            if row is None:
                raise DomainError("booking_not_found", "Reserva não encontrada.", 404)
            connection.execute("UPDATE bookings SET status = 'cancelled' WHERE id = ?", (booking_id,))
            return {**dict(row), "status": "cancelled"}
