import uuid
from unittest import TestCase

from app import app


class AppTestCase(TestCase):

    def setUp(self) -> None:
        app.config.update({"TESTING": True})
        self.client = app.test_client()
        return super().setUp()

    def test_reserve_error(self):
        response = self.client.post("/reserve")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid name"})

    def test_invalid_email(self):

        data = {
            "name": "test",
            "email": "fffff",
            "phone": "1231231234",
            "appointment_id": str(uuid.uuid4()),
        }

        response = self.client.post("/reserve", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid email format"})

    def test_invalid_appointment_id(self):
        data = {
            "name": "test",
            "email": "test@email.com",
            "phone": "1231231234",
            "appointment_id": "invalidddddddddd",
        }

        response = self.client.post("/reserve", json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid appointment_id format"})

    def test_success(self):
        data = {
            "name": "test",
            "email": "test@email.com",
            "phone": "1231231234",
            "appointment_id": str(uuid.uuid4()),
        }

        response = self.client.post("/reserve", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"appointment_id": data["appointment_id"]})
