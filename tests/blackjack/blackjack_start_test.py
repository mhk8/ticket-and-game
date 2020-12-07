from server import db
import json
import unittest
import unittest.mock as mock
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.models import Transaction, Blackjack
from server.utils.database_test import DatabaseTest
from server.utils import (
    mocked_random_org_call_norm,
    mocked_call_blackjack,
    mocked_bad_deck,
    mocked_local_deck,
)

KEY_SUCCESS = "success"
KEY_MESSAGE = "message"
KEY_AMOUNT = "amount"
KEY_BLACKJACK = "blackjack"
KEY_DEALER = "dealer"
KEY_PLAYER = "player"


class BlackjackStartTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        self.user2_id = 2
        trans1 = Transaction(
            user_id=self.user1_id,
            ticket_amount=500,
            activity="Transaction Test",
        )
        blackjack1 = Blackjack(
            user_id=self.user1_id, deck="[]", player_hand="[]", dealer_hand="[]"
        )
        with self.app.app_context():
            db.session.add(blackjack1)
            db.session.add(trans1)
            db.session.commit()

        self.blackjack_start_old_success = {
            KEY_SUCCESS: True,
            KEY_BLACKJACK: False,
            KEY_DEALER: ["2", "H"],
            KEY_PLAYER: ["3", "C", "5", "D"],
        }
        self.blackjack_start_new_success = {
            KEY_SUCCESS: True,
            KEY_BLACKJACK: True,
            KEY_DEALER: ["2", "H"],
            KEY_PLAYER: ["A", "D", "Q", "S"],
        }
        self.blackjack_bad_api_success = {
            KEY_SUCCESS: True,
            KEY_BLACKJACK: False,
            KEY_DEALER: ["A", "D"],
            KEY_PLAYER: ["2", "H", "4", "S"],
        }
        self.blackjack_start_error = {"error": "Malformed request"}

    def test_blackjack_start_old_success(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user1_id
            with mock.patch("requests.post", mocked_random_org_call_norm):
                res = self.client.post(
                    "/api/blackjack/start", data=json.dumps({KEY_AMOUNT: 500})
                )
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(self.blackjack_start_old_success, result)

    def test_blackjack_start_new_success(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user2_id
            with mock.patch("requests.post", mocked_call_blackjack):
                res = self.client.post(
                    "/api/blackjack/start", data=json.dumps({KEY_AMOUNT: 500})
                )
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(self.blackjack_start_new_success, result)

    def test_blackjack_start_bad(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user2_id
            with mock.patch("requests.post", mocked_bad_deck):
                with mock.patch("random.shuffle", mocked_local_deck):
                    res = self.client.post(
                        "/api/blackjack/start", data=json.dumps({KEY_AMOUNT: 500})
                    )
                    result = json.loads(res.data.decode("utf-8"))
                    self.assertDictEqual(self.blackjack_bad_api_success, result)

    def test_blackjack_start_error(self):
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.user2_id
        res = self.client.post("/api/blackjack/start", data="bad input")
        result = json.loads(res.data.decode("utf-8"))
        self.assertEqual(self.blackjack_start_error, result)
