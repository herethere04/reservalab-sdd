"""Casos de uso; o relógio injetável permite testes determinísticos."""

from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

from .domain import DomainError, validate_payload
from .repository import BookingRepository


class BookingService:
    """Interface da aplicação consumida pela API e pelos testes."""

    def __init__(self, db_path: str | Path, now: Callable[[], datetime] | None = None):
        self.repository = BookingRepository(db_path)
        self.now = now if now is not None else lambda: datetime.now(timezone.utc)

    def list_rooms(self) -> list[dict]:
        return self.repository.list_rooms()

    def create_booking(self, payload: object) -> dict:
        return self.repository.create_booking(validate_payload(payload, self.now()))

    def list_bookings(self) -> list[dict]:
        return self.repository.list_bookings()

    def cancel_booking(self, booking_id: str) -> dict:
        if not isinstance(booking_id, str) or not booking_id:
            raise DomainError("booking_not_found", "Reserva não encontrada.", 404)
        return self.repository.cancel_booking(booking_id)
