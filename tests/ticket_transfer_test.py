import json

from server import db
from server.utils.database_test import DatabaseTest
from server.utils import get_user_balance, get_user_by_id
from server.models import User, Transaction


class TicketTransferTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.sender_id = 1
        sender = User(id=self.sender_id, name="Sender", email="sender@example.com")
        self.receiver_id = 2
        receiver = User(
            id=self.receiver_id, name="Receiver", email="receiver@example.com"
        )

        with self.app.app_context():
            db.session.add(sender)
            db.session.add(receiver)
            transaction = Transaction(
                user=sender,
                ticket_amount=1000,
                activity="Transfer Test Initial Balance",
            )
            db.session.add(transaction)
            db.session.commit()

    def test_successful_transfer(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.sender_id

            sender = get_user_by_id(self.sender_id)
            receiver = get_user_by_id(self.receiver_id)

            amount = 10
            total_transfer = 0

            for _ in range(10):
                response = self.client.post(
                    "/api/ticket/transfer",
                    data=json.dumps({"to": receiver.id, "amount": amount}),
                )
                total_transfer += amount

                sender_balance = get_user_balance(sender.id)
                receiver_balance = get_user_balance(receiver.id)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(sender_balance, 1000 - total_transfer)
                self.assertEqual(receiver_balance, total_transfer)

    def test_insufficient_balance(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.sender_id

            sender = get_user_by_id(self.sender_id)
            receiver = get_user_by_id(self.receiver_id)

            amount = 1_000_000

            response = self.client.post(
                "/api/ticket/transfer",
                data=json.dumps({"to": receiver.id, "amount": amount}),
            )

            sender_balance = get_user_balance(sender.id)
            receiver_balance = get_user_balance(receiver.id)

            self.assertEqual(response.status_code, 400)
            self.assertEqual(sender_balance, 1000)
            self.assertEqual(receiver_balance, 0)

    def test_sending_to_self(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.sender_id

            sender = get_user_by_id(self.sender_id)
            receiver = get_user_by_id(self.receiver_id)

            amount = 10

            response = self.client.post(
                "/api/ticket/transfer",
                data=json.dumps({"to": sender.id, "amount": amount}),
            )

            sender_balance = get_user_balance(sender.id)
            receiver_balance = get_user_balance(receiver.id)

            self.assertEqual(response.status_code, 400)
            self.assertEqual(sender_balance, 1000)
            self.assertEqual(receiver_balance, 0)

    def test_send_to_nonexistent_user(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.sender_id

            sender = get_user_by_id(self.sender_id)
            sender_balance = get_user_balance(sender.id)

            amount = 100

            response = self.client.post(
                "/api/ticket/transfer",
                data=json.dumps({"to": 11111111, "amount": amount}),
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(sender_balance, 1000)

    def test_sending_negative_tickets(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.sender_id

            sender = get_user_by_id(self.sender_id)
            receiver = get_user_by_id(self.receiver_id)

            amount = -100

            response = self.client.post(
                "/api/ticket/transfer",
                data=json.dumps({"to": receiver.id, "amount": amount}),
            )

            sender_balance = get_user_balance(sender.id)
            receiver_balance = get_user_balance(receiver.id)

            self.assertEqual(response.status_code, 400)
            self.assertEqual(sender_balance, 1000)
            self.assertEqual(receiver_balance, 0)

    def test_send_malformed_request(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = self.sender_id

            response = self.client.post(
                "/api/ticket/transfer",
                data="bad request",
            )

            self.assertEqual(response.status_code, 400)