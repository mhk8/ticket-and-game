from server.models import Blackjack
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
KEY_BLACKJACK = "blackjack"
KEY_WINNER = "winner"
KEY_BUST = "bust"
KEY_PLAYER = "player"


class BlackjackHitTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        self.user2_id = 2
        self.user3_id = 3
        blackjack1 = Blackjack(
            user_id=self.user1_id,
            deck="[0, 1, 2]",
            player_hand="[6, 6]",
            dealer_hand="[2, 4]",
        )
        blackjack2 = Blackjack(
            user_id=self.user2_id,
            deck="[10, 2 , 3]",
            player_hand="[6, 6]",
            dealer_hand="[2, 4]",
        )
        blackjack3 = Blackjack(
            user_id=self.user3_id,
            deck="[6, 6]",
            player_hand="[6, 6]",
            dealer_hand="[2, 4]",
        )
        with self.app.app_context():
            db.session.add(blackjack1)
            db.session.add(blackjack2)
            db.session.add(blackjack3)
            db.session.commit()

        self.blackjack_hit_normal = {
            KEY_SUCCESS: True,
            KEY_BUST: False,
            KEY_BLACKJACK: False,
            KEY_PLAYER: ["7", "C", "7", "C", "A", "D"],
        }
        self.blackjack_hit_bust = {
            KEY_SUCCESS: True,
            KEY_BUST: True,
            KEY_WINNER: "Dealer",
            KEY_BLACKJACK: False,
            KEY_PLAYER: ["7", "C", "7", "C", "J", "C"],
        }
        self.blackjack_hit_blackjack = {
            KEY_SUCCESS: True,
            KEY_BUST: False,
            KEY_BLACKJACK: True,
            KEY_PLAYER: ["7", "C", "7", "C", "7", "C"],
        }

    def hit_path(self, user_id, hit_result):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = user_id
            with mock.patch("requests.post", mocked_random_org_call_norm):
                res = self.client.get("/api/blackjack/hit")
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(hit_result, result)

    def test_blackjack_hit(self):
        self.hit_path(self.user1_id, self.blackjack_hit_normal)
        self.hit_path(self.user2_id, self.blackjack_hit_bust)
        self.hit_path(self.user3_id, self.blackjack_hit_blackjack)
