import json
import unittest.mock as mock

from server import db
from server.models import User, Transaction
from server.utils.database_test import DatabaseTest
from server.utils import get_user_balance, get_user_by_id


COINFLIP_ENDPOINT = "/api/coinflip"


class CoinflipTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user_id = 1
        user = User(id=self.user_id, name="User", email="user@example.com")

        with self.app.app_context():
            db.session.add(user)
            transaction = Transaction(
                user=user, ticket_amount=1000, activity="Coinflip Test Initial Balance"
            )
            db.session.add(transaction)
            db.session.commit()

    def test_success_coinflip(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            amount = 100
            user = get_user_by_id(self.user_id)

            with mock.patch("server.routes.coinflip.randint", lambda _a, _b: 0):
                response = self.client.post(
                    COINFLIP_ENDPOINT,
                    data=json.dumps(
                        {
                            "side": "Heads",
                            "bet": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 1100)

                response = self.client.post(
                    COINFLIP_ENDPOINT,
                    data=json.dumps(
                        {
                            "side": "Tails",
                            "bet": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 1000)

            with mock.patch("server.routes.coinflip.randint", lambda _a, _b: 1):
                response = self.client.post(
                    COINFLIP_ENDPOINT,
                    data=json.dumps(
                        {
                            "side": "Tails",
                            "bet": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 1100)

                response = self.client.post(
                    COINFLIP_ENDPOINT,
                    data=json.dumps(
                        {
                            "side": "Heads",
                            "bet": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 1000)

    def test_fail_coinflip(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            amount = 10000
            user = get_user_by_id(self.user_id)

            with mock.patch("server.routes.coinflip.get_side", lambda: "Heads"):
                response = self.client.post(
                    COINFLIP_ENDPOINT,
                    data=json.dumps(
                        {
                            "side": "Tails",
                            "bet": amount,
                        }
                    ),
                )

                self.assertIn("error", response.json)
                self.assertEqual(1000, get_user_balance(user.id))

    def test_malformed_request(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            response = self.client.post(COINFLIP_ENDPOINT, data="bad_request")

            self.assertEqual(400, response.status_code)
