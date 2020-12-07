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
KEY_USERNAME = "username"
KEY_PASSWORD = "password"
KEY_USER_ID = "user_id"


def mocked_login():
    mocked_table = mock.Mock()
    mocked_table.filter().one.return_value = MockedLogin()
    return mocked_table


def mocked_user():
    mocked_table = mock.Mock()
    mocked_table.filter().one.return_value = MockedUser()
    return mocked_table


def mocked_query_search(table):
    if str(table) == "<class 'server.models.login.Login'>":
        return mocked_login()
    return mocked_user()


class MockedLogin:
    username = "username"
    password = (
        "b1b87c2429a3f77838faeae970c17a1b62e9b6a35fa9fd"
        "a4bc011bc39965849608d4377629c525bebc75c32ac372d135c"
        "d312c29f492d61bea7468893835c7c17c2f216a4490e10f67f6"
        "984cf4927f35ed43920873012cd854d7038dc92f7f56"
    )


class MockedUser:
    id = 1
    name = "name"
    username = "username"
    email = "email"


class PwdLoginTest(unittest.TestCase):
    def setUp(self):
        config = Config()
        config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        self.app = create_app(config)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

        self.success_test_bad_post = [{KEY_EXPECTED: {"error": "Malformed request"}}]
        self.success_test_bad_username_pwd = [
            {
                KEY_INPUT: "bad username",
                KEY_EXPECTED: {
                    KEY_SUCCESS: False,
                    KEY_MESSAGE: "Username does not exist or password is invalid.",
                },
            },
            {
                KEY_INPUT: "bad password",
                KEY_EXPECTED: {
                    KEY_SUCCESS: False,
                    KEY_MESSAGE: "Username does not exist or password is invalid.",
                },
            },
        ]
        self.success_test_valid_pwd = [
            {KEY_EXPECTED: {KEY_SUCCESS: True, KEY_USER_ID: 1}}
        ]

    def test_pwd_login_bad_post(self):
        for test_case in self.success_test_bad_post:
            res = self.client.post("/api/login/password", data="bad post")
            expected = test_case[KEY_EXPECTED]
            result = json.loads(res.data.decode("utf-8"))
            self.assertEqual(expected, result)

    def test_pwd_login_bad_username_pwd(self):
        for test_case in self.success_test_bad_username_pwd:
            with mock.patch("flask_sqlalchemy._QueryProperty.__get__") as mocked_query:
                if test_case[KEY_INPUT] == "bad username":
                    mocked_query.return_value.filter_by.return_value.scalar.return_value = (
                        None
                    )
                else:
                    mocked_query.return_value.filter_by.return_value.scalar.return_value = (
                        []
                    )
                with mock.patch("server.db.session.query", mocked_query_search):
                    res = self.client.post(
                        "/api/login/password",
                        data=json.dumps(
                            {KEY_USERNAME: "username", KEY_PASSWORD: "password"}
                        ),
                    )
                    expected = test_case[KEY_EXPECTED]
                    result = json.loads(res.data.decode("utf-8"))
                    self.assertDictEqual(expected, result)

    def test_pwd_login_success(self):
        for test_case in self.success_test_valid_pwd:
            with self.client as client:
                with client.session_transaction() as client_session:
                    client_session["user_id"] = 1
                with mock.patch(
                    "flask_sqlalchemy._QueryProperty.__get__"
                ) as mocked_query:
                    mocked_query.return_value.filter_by.return_value.scalar.return_value = (
                        []
                    )
                    with mock.patch("server.db.session.query", mocked_query_search):
                        res = self.client.post(
                            "/api/login/password",
                            data=json.dumps(
                                {KEY_USERNAME: "username", KEY_PASSWORD: "goodpassword"}
                            ),
                        )
                        expected = test_case[KEY_EXPECTED]
                        result = json.loads(res.data.decode("utf-8"))
                        self.assertDictEqual(expected, result)
