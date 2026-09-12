"""Testes HTTP reais: servidor local, porta efêmera e banco temporário."""

import http.client
import json
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from pathlib import Path

from reservalab.server import create_server


class HttpIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.server = create_server(
            Path(self.tempdir.name) / "http.sqlite3", host="127.0.0.1", port=0,
            now=lambda: datetime(2030, 1, 1, 8, tzinfo=timezone.utc))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def payload(self, **changes):
        payload = {"room_id": 1, "student_name": "Gabriel Ferreira Costa",
                   "starts_at": "2030-01-01T10:00:00Z", "ends_at": "2030-01-01T11:00:00Z",
                   "participants": 2}
        payload.update(changes)
        return payload

    def request(self, method, path, payload=None, raw=None, content_type="application/json"):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=10)
        try:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else raw
            headers = {"Content-Type": content_type} if body is not None else {}
            connection.request(method, path, body=body, headers=headers)
            response = connection.getresponse()
            raw_response = response.read()
            self.assertIn("application/json", response.getheader("Content-Type", ""))
            return response.status, json.loads(raw_response)
        finally:
            connection.close()

    def assert_error(self, response, status):
        actual_status, body = response
        self.assertEqual(actual_status, status, body)
        self.assertEqual(set(body), {"error"})
        self.assertTrue(body["error"]["code"])
        self.assertTrue(body["error"]["message"])

    def test_health_and_seed_rooms(self):
        self.assertEqual(self.request("GET", "/health"), (200, {"status": "ok"}))
        status, body = self.request("GET", "/rooms")
        self.assertEqual(status, 200)
        self.assertEqual({r["id"]: r["capacity"] for r in body["rooms"]}, {1: 4, 2: 8})

    def test_full_create_list_conflict_cancel_and_rebook_lifecycle(self):
        self.assertEqual(self.request("GET", "/bookings"), (200, {"bookings": []}))
        status, booking = self.request("POST", "/bookings", self.payload())
        self.assertEqual(status, 201)
        self.assertEqual(booking["status"], "active")
        self.assertEqual(self.request("GET", "/bookings"), (200, {"bookings": [booking]}))
        self.assert_error(self.request("POST", "/bookings", self.payload()), 409)
        status, cancelled = self.request("DELETE", f"/bookings/{booking['id']}")
        self.assertEqual(status, 200)
        self.assertEqual(cancelled["status"], "cancelled")
        self.assertEqual(self.request("DELETE", f"/bookings/{booking['id']}"), (200, cancelled))
        status, replacement = self.request("POST", "/bookings", self.payload())
        self.assertEqual(status, 201)
        self.assertNotEqual(replacement["id"], booking["id"])

    def test_json_validation_errors_are_structured(self):
        self.assert_error(self.request("POST", "/bookings", self.payload(participants=True)), 400)
        self.assert_error(self.request("POST", "/bookings", self.payload(extra="field")), 400)

    def test_malformed_json_is_rejected(self):
        self.assert_error(self.request("POST", "/bookings", raw=b'{"room_id":'), 400)

    def test_invalid_utf8_json_is_rejected(self):
        self.assert_error(self.request("POST", "/bookings", raw=b'\xff\xfe'), 400)

    def test_json_array_is_rejected(self):
        self.assert_error(self.request("POST", "/bookings", raw=b"[]"), 400)

    def test_nonfinite_json_numbers_are_rejected(self):
        for token in [b"NaN", b"Infinity", b"-Infinity"]:
            with self.subTest(token=token):
                self.assert_error(self.request("POST", "/bookings", raw=b'{"participants":' + token + b'}'), 400)

    def test_unpaired_unicode_surrogate_is_a_client_error(self):
        body = json.dumps(self.payload(student_name="AB\ud800")).encode("ascii")
        self.assert_error(self.request("POST", "/bookings", raw=body), 400)

    def test_enormous_unknown_room_id_is_a_client_error(self):
        self.assert_error(self.request("POST", "/bookings", self.payload(room_id=10 ** 100)), 404)

    def test_wrong_content_type_is_rejected(self):
        self.assert_error(self.request("POST", "/bookings", self.payload(), content_type="text/plain"), 415)

    def test_json_content_type_with_charset_is_accepted(self):
        status, body = self.request("POST", "/bookings", self.payload(),
                                    content_type="application/json; charset=utf-8")
        self.assertEqual(status, 201, body)

    def test_body_above_16_kib_is_rejected(self):
        self.assert_error(self.request("POST", "/bookings", raw=b"x" * (16 * 1024 + 1)), 413)

    def test_unknown_room_booking_and_route_return_not_found(self):
        self.assert_error(self.request("POST", "/bookings", self.payload(room_id=999)), 404)
        self.assert_error(self.request("DELETE", "/bookings/00000000-0000-0000-0000-000000000000"), 404)
        self.assert_error(self.request("GET", "/missing"), 404)

    def test_unsupported_method_returns_method_not_allowed(self):
        self.assert_error(self.request("PUT", "/bookings", self.payload()), 405)


if __name__ == "__main__":
    unittest.main()
