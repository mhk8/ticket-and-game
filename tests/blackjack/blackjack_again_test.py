from server.models import Transaction, Blackjack
from server.utils.database_test import DatabaseTest
from server.utils import mocked_random_org_call_norm
from server import db
import json
import unittest
import unittest.mock as mock
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


KEY_SUCCESS = "success"
KEY_AMOUNT = "amount"
KEY_BLACKJACK = "blackjack"
KEY_DEALER = "dealer"
KEY_PLAYER = "player"


class BlackjackAgainTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        trans1 = Transaction(
            user_id=self.user1_id,
            ticket_amount=500,
            activity="Transaction Test",
        )
        blackjack1 = Blackjack(
            user_id=self.user1_id,
            deck="[1, 2, 3, 4, 5]",
            player_hand="[1, 2]",
            dealer_hand="[1, 2]",
        )
        with self.app.app_context():
            db.session.add(blackjack1)
            db.session.add(trans1)
            db.session.commit()
        self.blackjack_again_success = {
            KEY_SUCCESS: True,
            KEY_BLACKJACK: False,
            KEY_DEALER: ["2", "H"],
            KEY_PLAYER: ["3", "C", "5", "D"],
        }
        self.blackjack_again_error = {"error": "Malformed request"}

    def test_blackjack_start_old_success(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user1_id
            with mock.patch("requests.post", mocked_random_org_call_norm):
                res = self.client.post(
                    "/api/blackjack/playagain", data=json.dumps({KEY_AMOUNT: 500})
                )
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(self.blackjack_again_success, result)

    def test_blackjack_again_error(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.user1_id
        res = self.client.post("/api/blackjack/playagain", data="bad input")
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(self.blackjack_again_error, result)
