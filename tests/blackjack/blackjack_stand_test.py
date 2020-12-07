from server.models import Blackjack, Transaction
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
KEY_WINNER = "winner"
KEY_DEALER = "dealer"
KEY_PLAYER = "player"
KEY_NONE = "none"


class BlackjackStandTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        self.user2_id = 2
        self.user3_id = 3
        trans1 = Transaction(
            user_id=self.user1_id,
            ticket_amount=-500,
            activity="blackjack",
        )
        blackjack1 = Blackjack(
            user_id=self.user1_id,
            deck="[0, 1, 2]",
            player_hand="[0, 12]",
            dealer_hand="[9, 5]",
        )
        blackjack2 = Blackjack(
            user_id=self.user2_id,
            deck="[6, 2 , 3]",
            player_hand="[0, 12]",
            dealer_hand="[6, 6]",
        )
        blackjack3 = Blackjack(
            user_id=self.user3_id,
            deck="[6, 6]",
            player_hand="[12, 12]",
            dealer_hand="[6, 6]",
        )
        with self.app.app_context():
            db.session.add(trans1)
            db.session.add(blackjack1)
            db.session.add(blackjack2)
            db.session.add(blackjack3)
            db.session.commit()

        self.blackjack_stand_win = {
            KEY_SUCCESS: True,
            KEY_WINNER: KEY_PLAYER,
            KEY_DEALER: ["0", "H", "6", "H", "A", "D", "2", "H"],
            KEY_PLAYER: ["A", "D", "K", "D"],
        }
        self.blackjack_stand_tie = {
            KEY_SUCCESS: True,
            KEY_WINNER: KEY_NONE,
            KEY_DEALER: ["7", "C", "7", "C", "7", "C"],
            KEY_PLAYER: ["A", "D", "K", "D"],
        }
        self.blackjack_stand_lose = {
            KEY_SUCCESS: True,
            KEY_WINNER: KEY_DEALER,
            KEY_DEALER: ["7", "C", "7", "C", "7", "C"],
            KEY_PLAYER: ["K", "D", "K", "D"],
        }

    def stand_path(self, user_id, hit_result):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = user_id
            with mock.patch("requests.post", mocked_random_org_call_norm):
                res = self.client.get("/api/blackjack/stand")
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(hit_result, result)

    def test_blackjack_stand(self):
        self.stand_path(self.user1_id, self.blackjack_stand_win)
        self.stand_path(self.user2_id, self.blackjack_stand_tie)
        self.stand_path(self.user3_id, self.blackjack_stand_lose)
