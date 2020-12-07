import json
import unittest.mock as mock

from server import db
from server.models import User, Transaction
from server.utils.database_test import DatabaseTest
from server.utils import get_user_balance, get_user_by_id


COINFLIP_ENDPOINT = "/api/skiball"


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

    def test_success_skiball(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            user = get_user_by_id(self.user_id)
            balance = 1000
            amounts = [10, 20, 30, 40, 50, 100]

            for amount in amounts:
                with mock.patch("random.choice", lambda _b: amount):
                    response = self.client.post(COINFLIP_ENDPOINT)
                    balance -= 30
                    balance += amount

                    self.assertEqual(response.json["amount"], amount)
                    self.assertEqual(get_user_balance(user.id), balance)

    def test_fail_coinflip(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            user = get_user_by_id(self.user_id)

            transaction = Transaction(
                user=user, ticket_amount=-1000, activity="Make balance 0"
            )
            db.session.add(transaction)
            db.session.commit()

            response = self.client.post(COINFLIP_ENDPOINT)

            self.assertIn("error", response.json)
