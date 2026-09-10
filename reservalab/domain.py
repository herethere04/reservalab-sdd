"""Erros e validações independentes de HTTP e persistência."""

from datetime import datetime, timezone
import re


class DomainError(Exception):
    """Falha esperada, com código estável e status da resposta HTTP."""

    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


REQUIRED_FIELDS = {"room_id", "student_name", "starts_at", "ends_at", "participants"}
TIMESTAMP = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}"
    r"(?::(?P<seconds>\d{2})(?:\.(?P<fraction>\d+))?)?"
    r"(?:[Zz]|[+-](?:[01]\d|2[0-3]):[0-5]\d)$"
)


def parse_datetime(value: object, field: str) -> datetime:
    """Aceita data/hora ISO com fuso explícito e precisão de minutos."""
    match = TIMESTAMP.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        raise DomainError("invalid_datetime", f"{field} exige data/hora ISO com fuso explícito.")
    seconds = match.group("seconds")
    fraction = match.group("fraction")
    if (seconds is not None and seconds != "00") or (fraction and any(c != "0" for c in fraction)):
        raise DomainError("invalid_datetime", f"{field} deve usar minutos inteiros (segundos iguais a zero).")
    try:
        parsed = datetime.fromisoformat(value.upper().replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError) as exc:
        raise DomainError("invalid_datetime", f"{field} contém data/hora inválida.") from exc


def format_datetime(value: datetime) -> str:
    """Serializa UTC em formato estável, também ordenável no SQLite."""
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_payload(payload: object, now: datetime) -> dict:
    """Valida dados independentes da sala e devolve valores normalizados."""
    if not isinstance(payload, dict) or set(payload) != REQUIRED_FIELDS:
        raise DomainError(
            "invalid_payload",
            "Informe exatamente room_id, student_name, starts_at, ends_at e participants.",
        )
    room_id = payload["room_id"]
    if type(room_id) is not int or room_id < 1:
        raise DomainError("invalid_room_id", "room_id deve ser um inteiro positivo.")
    name = payload["student_name"]
    if not isinstance(name, str) or not 2 <= len(name.strip()) <= 100:
        raise DomainError("invalid_student_name", "student_name deve ter entre 2 e 100 caracteres após remover espaços externos.")
    try:
        name.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise DomainError("invalid_student_name", "student_name deve conter caracteres Unicode válidos.") from exc
    participants = payload["participants"]
    if type(participants) is not int or participants < 1:
        raise DomainError("invalid_participants", "participants deve ser um inteiro positivo.")
    start = parse_datetime(payload["starts_at"], "starts_at")
    end = parse_datetime(payload["ends_at"], "ends_at")
    duration = (end - start).total_seconds() / 60
    if not 30 <= duration <= 120:
        raise DomainError("invalid_duration", "A reserva deve durar entre 30 e 120 minutos.")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("O relógio da aplicação deve fornecer datetime com fuso horário.")
    if start < now:
        raise DomainError("start_in_past", "O início da reserva não pode estar no passado.")
    return {
        "room_id": room_id,
        "student_name": name.strip(),
        "starts_at": format_datetime(start),
        "ends_at": format_datetime(end),
        "participants": participants,
    }
