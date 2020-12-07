from config import Config
from server import db, create_app
import json
import unittest
import unittest.mock as mock
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_SUCCESS = "success"
KEY_MESSAGE = "message"
KEY_NAME = "name"
KEY_USERNAME = "username"
KEY_EMAIL = "email"
KEY_PASSWORD = "password"


class SignUpTest(unittest.TestCase):
    def setUp(self):
        config = Config()
        config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        self.app = create_app(config)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

        self.success_test_params_error = [
            {
                KEY_INPUT: "same email",
                KEY_EXPECTED: {
                    KEY_SUCCESS: False,
                    KEY_MESSAGE: "Another account seems to be using the same email.",
                },
            },
            {
                KEY_INPUT: "same username",
                KEY_EXPECTED: {
                    KEY_SUCCESS: False,
                    KEY_MESSAGE: "Username has already been taken please try another username",
                },
            },
        ]
        self.success_test_data_error = [{KEY_EXPECTED: {"error": "Malformed request"}}]
        self.success_test_params = [{KEY_EXPECTED: {"success": True, "user_id": None}}]

    def test_signup_same_user(self):
        for test_case in self.success_test_params_error:
            with mock.patch("flask_sqlalchemy._QueryProperty.__get__") as mocked_query:
                if test_case[KEY_INPUT] == "same email":
                    mocked_query.return_value.filter_by.return_value.scalar.return_value = (
                        []
                    )
                else:
                    mocked_double_query = [mock.Mock(), mock.Mock()]
                    mocked_double_query[
                        0
                    ].filter_by.return_value.scalar.return_value = None
                    mocked_double_query[
                        1
                    ].filter_by.return_value.scalar.return_value = []
                    mocked_query.side_effect = mocked_double_query
                res = self.client.post(
                    "/api/signup/password",
                    data=json.dumps(
                        {
                            KEY_NAME: "allen",
                            KEY_USERNAME: "username",
                            KEY_EMAIL: "email",
                            KEY_PASSWORD: "password",
                        }
                    ),
                )
                expected = test_case[KEY_EXPECTED]
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(expected, result)

    def test_signup_bad_input(self):
        for test_case in self.success_test_data_error:
            res = self.client.post("/api/signup/password", data="bad input")
            expected = test_case[KEY_EXPECTED]
            result = json.loads(res.data.decode("utf-8"))
            self.assertEqual(expected, result)

    def test_signup_success_input(self):
        for test_case in self.success_test_params:
            with self.client as client:
                with client.session_transaction() as client_session:
                    client_session["user_id"] = 1
                with mock.patch(
                    "flask_sqlalchemy._QueryProperty.__get__"
                ) as mocked_query:
                    mocked_query.return_value.filter_by.return_value.scalar.return_value = (
                        None
                    )
                    with mock.patch(
                        "server.db.session.add",
                    ):
                        with mock.patch(
                            "server.db.session.commit",
                        ):
                            res = client.post(
                                "/api/signup/password",
                                data=json.dumps(
                                    {
                                        KEY_NAME: "name",
                                        KEY_USERNAME: "username",
                                        KEY_EMAIL: "email",
                                        KEY_PASSWORD: "password",
                                    }
                                ),
                            )
                    expected = test_case[KEY_EXPECTED]
                    result = json.loads(res.data.decode("utf-8"))
                    self.assertDictEqual(expected, result)
            with self.client.session_transaction() as client_session:
                client_session.clear()
