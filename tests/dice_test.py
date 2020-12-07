import json
import unittest.mock as mock

from server import db
from server.models import User, Transaction
from server.utils.database_test import DatabaseTest
from server.utils import get_user_balance, get_user_by_id


DICE_ENDPOINT = "/api/dice"


class DiceTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user_id = 1
        user = User(id=self.user_id, name="User", email="user@example.com")

        with self.app.app_context():
            db.session.add(user)
            transaction = Transaction(
                user=user, ticket_amount=1000, activity="Dice Test Initial Balance"
            )
            db.session.add(transaction)
            db.session.commit()

    def test_success_dice(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            amount = 100
            user = get_user_by_id(self.user_id)

            with mock.patch("server.routes.dice.randint", lambda _a, _b: 1):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 1,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 400 points
                self.assertEqual(get_user_balance(user.id), 1400)

                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 2,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 1300)
            with mock.patch("server.routes.dice.randint", lambda _a, _b: 2):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 2,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 1700)

                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 3,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 1600)
            with mock.patch("server.routes.dice.randint", lambda _a, _b: 3):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 3,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 2000)

                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 4,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 1900)
            with mock.patch("server.routes.dice.randint", lambda _a, _b: 4):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 4,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 2300)

                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 5,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 2200)
            with mock.patch("server.routes.dice.randint", lambda _a, _b: 5):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 5,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 2600)

                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 6,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 2500)
            with mock.patch("server.routes.dice.randint", lambda _a, _b: 6):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 6,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertTrue(response.json["won"])  # Win 100 points
                self.assertEqual(get_user_balance(user.id), 2900)

                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 1,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertFalse(response.json["won"])  # Lose 100 points
                self.assertEqual(get_user_balance(user.id), 2800)

    def test_fail_dice(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            amount = 10000
            user = get_user_by_id(self.user_id)

            with mock.patch("server.routes.dice.get_side", lambda: 2):
                response = self.client.post(
                    DICE_ENDPOINT,
                    data=json.dumps(
                        {
                            "bet": 6,
                            "quantity": amount,
                        }
                    ),
                )

                self.assertIn("error", response.json)
                self.assertEqual(1000, get_user_balance(user.id))

    def test_malformed_request(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user_id

            response = self.client.post(DICE_ENDPOINT, data="bad_request")

            self.assertEqual(400, response.status_code)
