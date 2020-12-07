import datetime

from server import db
from server.utils.database_test import DatabaseTest
from server.models import User


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_NAME = "name"
KEY_USERNAME = "username"
KEY_REGISTRATION = "registration_datetime"
KEY_TOTAL_TICKETS = "total_tickets"


class ProfileViewTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user_id = 1
        self.registration_time = datetime.datetime.utcnow()
        user = User(
            id=self.user_id,
            name="Current user",
            email="user@example.com",
            registration_datetime=self.registration_time,
            is_public=False,
        )
        self.other_user_id = 2
        other_user = User(
            id=self.other_user_id,
            name="Other user",
            email="otheruser@example.com",
            registration_datetime=self.registration_time,
            is_public=True,
        )
        self.private_user_id = 3
        private_user = User(
            id=self.private_user_id,
            name="Private user",
            email="privateuser@example.com",
            registration_datetime=self.registration_time,
            is_public=False,
        )

        with self.app.app_context():
            db.session.add(user)
            db.session.add(other_user)
            db.session.add(private_user)
            db.session.commit()

    def test_success_profile_view(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = 1

            response = self.client.get("/api/profile/")
            self.assertEqual(response.json[KEY_NAME], "Current user")

    def test_other_successful_profile_view(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            response = self.client.get(f"/api/profile/{self.other_user_id}")
            self.assertEqual(response.json[KEY_NAME], "Other user")

    def test_other_user_not_found(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            response = self.client.get(f"/api/profile/{3333333}")
            self.assertEqual(response.status_code, 404)

    def test_private_user_not_accessible(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            response = self.client.get(f"/api/profile/{self.private_user_id}")
            self.assertEqual(response.status_code, 401)
