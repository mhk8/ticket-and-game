import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.sql import func
from server import db
from server.utils.database_test import DatabaseTest
from server.models import User, Transaction

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_USER = "user"
KEY_SUCCESS = "success"
KEY_MESSAGE = "message"
KEY_USER_ID = "user_id"
KEY_AMOUNT = 1000

class OauthNewUser(DatabaseTest):
    def setUp(self):
        super().setUp()
        user1 = User (
            oauth_id="password",
            name="test",
            username="test",
            email="test@gmail.com"
        )
        user2 = User (
            oauth_id="google",
            name="test",
            email="goodtest@gmail.com"
        )
        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()
        self.success_test_params_user = [
        {
            KEY_INPUT: {KEY_USER: "test"},
            KEY_EXPECTED: {
                KEY_SUCCESS: False,
                KEY_MESSAGE: "Username already exist. please try another one."
            }
        },
        {
            KEY_INPUT: {KEY_USER: "goodtest"},
            KEY_EXPECTED: {
                KEY_SUCCESS: True,
                KEY_USER_ID: 1
            }
        }]
        self.success_test_params_error = {"error": "Malformed request"}

    def test_new_user_success(self):
        for test_case in self.success_test_params_user:
            with self.app.app_context():
                with self.client.session_transaction() as sess:
                    sess['user_id'] = 1
                res = self.client.post(
                    '/api/login/newuser',
                    data = json.dumps(test_case[KEY_INPUT])
                )
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(test_case[KEY_EXPECTED], result)
                if result["success"] is True:
                    self.assertEqual(
                        KEY_AMOUNT,
                        db.session.query(func.sum(Transaction.ticket_amount))
                        .filter(Transaction.user_id == 1)
                        .scalar()
                    )

    def test_new_user_error(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess['user_id'] = 1
            res = self.client.post(
                '/api/login/newuser',
                data = "Bad input"
            )
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(self.success_test_params_error, result)
