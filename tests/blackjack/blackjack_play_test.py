import json

from server.models import Transaction
from server.utils.database_test import DatabaseTest
from server import db

KEY_SUCCESS = "success"
KEY_MESSAGE = "message"
KEY_ERROR = "error"


class BlackjackPlayTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        self.user2_id = 2
        self.user3_id = 3
        trans1 = Transaction(
            user_id=self.user1_id,
            ticket_amount=500,
            activity="Transaction Test",
        )
        trans2 = Transaction(
            user_id=self.user2_id,
            ticket_amount=400,
            activity="Transaction Test",
        )
        with self.app.app_context():
            db.session.add(trans1)
            db.session.add(trans2)
            db.session.commit()

        self.blackjack_play_success = {
            KEY_SUCCESS: True,
            KEY_MESSAGE: "Welcome to Blackjack!",
        }
        self.blackjack_play_bad_user = {
            KEY_ERROR: "User not logged in",
        }
        self.blackjack_play_bad_funds = {
            KEY_SUCCESS: False,
            KEY_MESSAGE: "Client needs at least 500 tickets to play.",
        }

    def test_blackjack_success(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user1_id
            res = self.client.get("/api/blackjack/play")
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(self.blackjack_play_success, result)

    def test_blackjack_bad_funds(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user2_id
            res = self.client.get("/api/blackjack/play")
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(self.blackjack_play_bad_funds, result)

    def test_blackjack_no_funds(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.user3_id
            res = self.client.get("/api/blackjack/play")
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(self.blackjack_play_bad_funds, result)

    def test_blackjack_bad_user(self):
        res = self.client.get("/api/blackjack/play")
        result = json.loads(res.data.decode("utf-8"))
        self.assertDictEqual(self.blackjack_play_bad_user, result)
