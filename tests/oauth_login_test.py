import unittest.mock as mock
import json
import os
import sys

from server import db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.utils.database_test import DatabaseTest
from server.models.user import User

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_DATABASE = "database"

def mocked_token_info(sub):
    return {
        "iss": "https://accounts.google.com",
        "sub": sub,
        "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
        "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
        "iat": "1433978353",
        "exp": "1433981953",
        "email": "testuser@gmail.com",
        "email_verified": "true",
        "name": "Test User",
        "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
        "given_name": "Test",
        "family_name": "User",
        "locale": "en",
    }


class MockedTransData:
    id = 1
    datetime = "Tue, 10 Nov 2020 18:19:43 GMT"
    activity = "COINFILP"
    ticket_amount = 50


class OauthLoginTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.success_test_params_user = [
            {
                KEY_INPUT: json.dumps({"token": "google_oauth_token"}),
                KEY_DATABASE: User (
                    oauth_id="google",
                    name="Test User",
                    username="Test",
                    email="testuser@gmail.com"
                )
            },
            {
                KEY_INPUT: json.dumps({"token": "google_oauth_token"}),
                KEY_DATABASE: User (
                    oauth_id="google",
                    name="Test User",
                    email="testuser@gmail.com"
                )
            },
            {
                KEY_INPUT: json.dumps({"token": "google_oauth_token"}),
                KEY_DATABASE: User (
                    oauth_id="google",
                    name="Other user",
                    email="otheruser@gmail.com"
                )
            }
        ]
        self.fail_test_params_user = [
            {
                KEY_INPUT: json.dumps({"token": "google_oauth_token"}),
                KEY_EXPECTED: "Invalid Value",
            },
            {
                KEY_INPUT: "{bad_json_string}",
                KEY_EXPECTED: "Malformed request",
            },
        ]

    def user_table_reset(self):
        db.session.query(User).delete()
        db.session.commit()

    def test_success_transaction_history(self):
        for test_case in self.success_test_params_user:
            with self.app.app_context():
                self.user_table_reset()
                db.session.add(test_case[KEY_DATABASE])
                db.session.commit()
                with mock.patch("server.routes.user.get_token_info", mocked_token_info):
                    response = self.client.post(
                        "/api/login/oauth", data=test_case[KEY_INPUT]
                    )
                    self.assertIn("success", response.json)

    def test_fail_oauth_login(self):
        for test_case in self.fail_test_params_user:
            with self.app.app_context():
                response = self.client.post("/api/login/oauth", data=test_case[KEY_INPUT])
                self.assertIn("error", response.json)
                self.assertEqual(test_case[KEY_EXPECTED], response.json["error"])
