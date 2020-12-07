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
KEY_DEALER = "dealer"
KEY_PLAYER = "player"


class BlackjackStandTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        blackjack1 = Blackjack(
            user_id=self.user1_id,
            deck="[6, 0, 6, 12]",
            player_hand="[0, 12]",
            dealer_hand="[9, 5]",
        )
        with self.app.app_context():
            db.session.add(blackjack1)
            db.session.commit()

        self.blackjack_tie_success = {
            KEY_SUCCESS: True,
            KEY_BLACKJACK: True,
            KEY_DEALER: ["7", "C"],
            KEY_PLAYER: ["A", "D", "K", "D"],
        }

    def test_tie_success(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user1_id
            with mock.patch("requests.post", mocked_random_org_call_norm):
                res = self.client.get("/api/blackjack/tiebreaker")
                result = json.loads(res.data.decode("utf-8"))
                self.assertDictEqual(self.blackjack_tie_success, result)
