"""Regras de negócio, isolamento, persistência e concorrência em SQLite real."""

import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from reservalab.domain import DomainError
from reservalab.service import BookingService


NOW = datetime(2030, 1, 1, 8, 0, tzinfo=timezone.utc)


class BookingServiceTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.db_path = Path(self.tempdir.name) / "bookings.sqlite3"
        self.service = BookingService(self.db_path, now=lambda: NOW)

    def payload(self, **changes):
        result = {
            "room_id": 1,
            "student_name": "Áquila de Brito Barbosa",
            "starts_at": "2030-01-01T10:00:00Z",
            "ends_at": "2030-01-01T11:00:00Z",
            "participants": 4,
        }
        result.update(changes)
        return result

    def assert_rejected(self, payload, status=400):
        with self.assertRaises(DomainError) as caught:
            self.service.create_booking(payload)
        self.assertEqual(caught.exception.status, status)
        self.assertIsInstance(caught.exception.code, str)
        self.assertTrue(caught.exception.message)
        return caught.exception

    def test_seed_rooms_have_documented_capacities(self):
        rooms = self.service.list_rooms()
        self.assertEqual({room["id"]: room["capacity"] for room in rooms}, {1: 4, 2: 8})

    def test_new_database_starts_without_bookings(self):
        self.assertEqual(self.service.list_bookings(), [])

    def test_create_returns_uuid_and_normalized_booking(self):
        booking = self.service.create_booking(self.payload(student_name="  Áquila de Brito Barbosa  "))
        UUID(booking["id"])
        self.assertEqual(booking["room_id"], 1)
        self.assertEqual(booking["student_name"], "Áquila de Brito Barbosa")
        self.assertEqual(booking["starts_at"], "2030-01-01T10:00:00Z")
        self.assertEqual(booking["ends_at"], "2030-01-01T11:00:00Z")
        self.assertEqual(booking["participants"], 4)
        self.assertEqual(booking["status"], "active")
        self.assertEqual(self.service.list_bookings(), [booking])

    def test_timezone_offset_is_normalized_to_utc(self):
        booking = self.service.create_booking(self.payload(
            starts_at="2030-01-01T07:00:00-03:00", ends_at="2030-01-01T08:00:00-03:00"))
        self.assertEqual(booking["starts_at"], "2030-01-01T10:00:00Z")
        self.assertEqual(booking["ends_at"], "2030-01-01T11:00:00Z")

    def test_start_equal_to_now_is_allowed(self):
        booking = self.service.create_booking(self.payload(
            starts_at="2030-01-01T08:00:00Z", ends_at="2030-01-01T08:30:00Z"))
        self.assertEqual(booking["status"], "active")

    def test_start_before_now_is_rejected(self):
        self.assert_rejected(self.payload(starts_at="2030-01-01T07:59:00Z", ends_at="2030-01-01T08:59:00Z"))

    def test_minimum_duration_30_minutes_is_allowed(self):
        self.service.create_booking(self.payload(ends_at="2030-01-01T10:30:00Z"))

    def test_maximum_duration_120_minutes_is_allowed(self):
        self.service.create_booking(self.payload(ends_at="2030-01-01T12:00:00Z"))

    def test_duration_outside_bounds_is_rejected(self):
        for end in ["10:00", "09:59", "10:29", "12:01"]:
            with self.subTest(end=end):
                self.assert_rejected(self.payload(ends_at=f"2030-01-01T{end}:00Z"))
        self.assertEqual(self.service.list_bookings(), [])

    def test_overlap_shapes_are_rejected(self):
        self.service.create_booking(self.payload())
        for start, end in [("10:00", "11:00"), ("09:30", "10:30"),
                           ("10:30", "11:30"), ("09:30", "11:30"),
                           ("10:15", "10:45")]:
            with self.subTest(start=start, end=end):
                error = self.assert_rejected(self.payload(
                    starts_at=f"2030-01-01T{start}:00Z",
                    ends_at=f"2030-01-01T{end}:00Z"), status=409)
                self.assertEqual(error.code, "booking_conflict")
        self.assertEqual(len(self.service.list_bookings()), 1)

    def test_offset_equivalent_time_also_conflicts(self):
        self.service.create_booking(self.payload())
        self.assert_rejected(self.payload(starts_at="2030-01-01T07:00:00-03:00",
                                          ends_at="2030-01-01T08:00:00-03:00"), status=409)

    def test_adjacent_bookings_are_allowed_on_both_sides(self):
        self.service.create_booking(self.payload())
        self.service.create_booking(self.payload(starts_at="2030-01-01T09:00:00Z",
                                                  ends_at="2030-01-01T10:00:00Z"))
        self.service.create_booking(self.payload(starts_at="2030-01-01T11:00:00Z",
                                                  ends_at="2030-01-01T12:00:00Z"))
        self.assertEqual(len(self.service.list_bookings()), 3)

    def test_same_slot_in_different_rooms_is_allowed(self):
        self.service.create_booking(self.payload())
        self.service.create_booking(self.payload(room_id=2, participants=8))
        self.assertEqual(len(self.service.list_bookings()), 2)

    def test_participants_capacity_limits(self):
        for value in [0, -1, 5, True, False, 1.0, "1", None]:
            with self.subTest(value=value):
                self.assert_rejected(self.payload(participants=value))

    def test_one_participant_is_allowed(self):
        self.assertEqual(self.service.create_booking(self.payload(participants=1))["participants"], 1)

    def test_room_id_requires_integer_not_boolean(self):
        for value in [True, False, 1.0, "1", None, [], {}]:
            with self.subTest(value=value):
                self.assert_rejected(self.payload(room_id=value))

    def test_unknown_room_is_not_found(self):
        self.assert_rejected(self.payload(room_id=999), status=404)

    def test_room_id_above_sqlite_integer_range_is_not_found(self):
        self.assert_rejected(self.payload(room_id=10 ** 100), status=404)

    def test_invalid_timezone_offset_minutes_are_rejected(self):
        for offset in ["+00:60", "-03:60"]:
            with self.subTest(offset=offset):
                self.assert_rejected(self.payload(starts_at=f"2030-01-01T10:00:00{offset}",
                                                  ends_at=f"2030-01-01T11:00:00{offset}"))

    def test_unpaired_surrogate_in_student_name_is_rejected(self):
        self.assert_rejected(self.payload(student_name="AB\ud800"))

    def test_student_name_limits_and_type(self):
        for value in ["", " ", "A", " A ", "A" * 101, None, 42, [], {}]:
            with self.subTest(value=value):
                self.assert_rejected(self.payload(student_name=value))

    def test_student_name_length_boundaries_are_allowed(self):
        self.service.create_booking(self.payload(student_name="AB"))
        self.service.create_booking(self.payload(student_name="A" * 100, room_id=2))
        self.assertEqual(len(self.service.list_bookings()), 2)

    def test_every_required_field_must_be_present(self):
        for key in self.payload():
            with self.subTest(missing=key):
                payload = self.payload()
                del payload[key]
                self.assert_rejected(payload)

    def test_unknown_fields_are_rejected(self):
        self.assert_rejected(self.payload(status="cancelled"))
        self.assert_rejected(self.payload(id="user-controlled-id"))

    def test_non_object_payloads_are_rejected(self):
        for value in [None, [], "text", 5, True]:
            with self.subTest(value=value):
                self.assert_rejected(value)

    def test_invalid_or_naive_timestamps_are_rejected_for_both_fields(self):
        values = ["invalid", "2030-02-30T10:00:00Z", "2030-01-01",
                  "2030-01-01T10:00:00", "2030-01-01T25:00:00Z",
                  "2030-01-01T10:00:00+25:00", "", None, 123]
        for field in ["starts_at", "ends_at"]:
            for value in values:
                with self.subTest(field=field, value=value):
                    self.assert_rejected(self.payload(**{field: value}))

    def test_non_whole_minutes_are_rejected_for_both_fields(self):
        for field in ["starts_at", "ends_at"]:
            for time in ["10:00:01Z", "10:00:00.000001Z", "10:00:30-03:00"]:
                with self.subTest(field=field, time=time):
                    self.assert_rejected(self.payload(**{field: f"2030-01-01T{time}"}))

    def test_cancel_is_idempotent_and_keeps_audit_record(self):
        booking = self.service.create_booking(self.payload())
        cancelled = self.service.cancel_booking(booking["id"])
        self.assertEqual(cancelled["status"], "cancelled")
        self.assertEqual(cancelled["id"], booking["id"])
        self.assertEqual(self.service.cancel_booking(booking["id"]), cancelled)
        self.assertEqual(self.service.list_bookings(), [cancelled])

    def test_cancel_frees_slot_for_new_booking(self):
        first = self.service.create_booking(self.payload())
        self.service.cancel_booking(first["id"])
        second = self.service.create_booking(self.payload())
        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(second["status"], "active")
        self.assertEqual(len(self.service.list_bookings()), 2)

    def test_cancel_unknown_booking_returns_not_found(self):
        with self.assertRaises(DomainError) as caught:
            self.service.cancel_booking("00000000-0000-0000-0000-000000000000")
        self.assertEqual(caught.exception.status, 404)

    def test_bookings_and_cancellations_persist_on_reopen(self):
        active = self.service.create_booking(self.payload())
        cancelled = self.service.create_booking(self.payload(room_id=2))
        self.service.cancel_booking(cancelled["id"])
        reopened = BookingService(self.db_path, now=lambda: NOW)
        rows = {row["id"]: row for row in reopened.list_bookings()}
        self.assertEqual(rows[active["id"]], active)
        self.assertEqual(rows[cancelled["id"]]["status"], "cancelled")
        self.assertEqual(len(reopened.list_rooms()), 2)

    def test_concurrent_same_slot_has_exactly_one_winner(self):
        workers = 6
        services = [BookingService(self.db_path, now=lambda: NOW) for _ in range(workers)]
        barrier = threading.Barrier(workers)

        def book(service):
            barrier.wait(timeout=10)
            try:
                service.create_booking(self.payload())
                return 201
            except DomainError as error:
                return error.status

        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(book, services))
        self.assertEqual(results.count(201), 1, results)
        self.assertEqual(results.count(409), workers - 1, results)
        self.assertEqual(len(self.service.list_bookings()), 1)


if __name__ == "__main__":
    unittest.main()
