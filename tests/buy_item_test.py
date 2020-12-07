import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import db
from sqlalchemy.sql import func
from server.utils.database_test import DatabaseTest
from server.models import Transaction, Item, Store

KEY_SUCCESS = "success"
KEY_MESSAGE = "message"
KEY_ERROR = "error"
KEY_ID = "id"
KEY_QUANTITY = "quantity"
KEY_EXPECTED = "expected"
KEY_PARAMS = "parameters"
KEY_USER_ID = "user_id"
KEY_AMOUNT = "AMOUNT"

class BuyItemTest(DatabaseTest):
    def setUp(self):
        super().setUp()
        self.user1_id = 1
        self.user2_id = 2
        self.user3_id = 3
        trans1 = Transaction (
            user_id=self.user1_id,
            ticket_amount=1500,
            activity="Transaction Test",
        )
        trans2 = Transaction (
            user_id=self.user2_id,
            ticket_amount=500,
            activity="Transaction Test",
        )
        store_item1 = Store (
            name="test item1",
            item_group=1,
            price=1000,
            limit=5,
        )
        store_item2 = Store (
            name="test item2",
            item_group=2,
            price=500,
            limit=1,
        )
        item1 = Item (
            item_type=1,
            item_group=1,
            user_id=self.user1_id,
            count=1,
            active=False
        )
        item2 = Item (
            item_type=2,
            item_group=2,
            user_id=self.user2_id,
            count=1,
            active=False
        )
        with self.app.app_context():
            db.session.add(trans1)
            db.session.add(trans2)
            db.session.add(store_item1)
            db.session.add(store_item2)
            db.session.add(item1)
            db.session.add(item2)
            db.session.commit()
        self.params_item1 = {
            KEY_ID: 1,
            KEY_QUANTITY: 1
        }
        self.buy_item_bad_funds = {
            KEY_SUCCESS: False,
            KEY_MESSAGE: "Insufficient funds"
        }
        self.buy_item_bad_item = {
            KEY_SUCCESS: False,
            KEY_MESSAGE: "Reached purchase limit"
        }
        self.params_item2 = {
            KEY_ID: 2,
            KEY_QUANTITY: 1
        }
        self.buy_item_params = [
        {
            KEY_USER_ID: self.user1_id,
            KEY_PARAMS: self.params_item1,
            KEY_AMOUNT: 500,
            KEY_EXPECTED: { KEY_SUCCESS: True }
        },
        {
            KEY_USER_ID: self.user1_id,
            KEY_PARAMS: self.params_item2,
            KEY_AMOUNT: 0,
            KEY_EXPECTED: { KEY_SUCCESS: True }
        },
        {
            KEY_USER_ID: self.user2_id,
            KEY_PARAMS: self.params_item1,
            KEY_AMOUNT: 500,
            KEY_EXPECTED: self.buy_item_bad_funds
        },
        {
            KEY_USER_ID: self.user3_id,
            KEY_PARAMS: self.params_item1,
            KEY_AMOUNT: None,
            KEY_EXPECTED: self.buy_item_bad_funds
        },
        {
            KEY_USER_ID: self.user2_id,
            KEY_PARAMS: self.params_item2,
            KEY_AMOUNT: 500,
            KEY_EXPECTED: self.buy_item_bad_item
        }]
        self.buy_item_error = {
            KEY_ERROR: "Malformed request"
        }

    def buy_item_test(self, test_case):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess['user_id'] = test_case[KEY_USER_ID]
            res = self.client.post('/api/store/buy', data = json.dumps(test_case[KEY_PARAMS]))
            result = json.loads(res.data.decode("utf-8"))
            self.assertDictEqual(test_case[KEY_EXPECTED], result)
            self.assertEqual(
                test_case[KEY_AMOUNT],
                db.session.query(func.sum(Transaction.ticket_amount))
                .filter(Transaction.user_id == test_case[KEY_USER_ID])
                .scalar()
            )

    def test_buy_item_success(self):
        for test_case in self.buy_item_params:
            self.buy_item_test(test_case)
    
    def test_buy_item_error(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess['user_id'] = self.user1_id
            res = self.client.post('/api/store/buy', data = "bad data")
            result = json.loads(res.data.decode("utf-8"))
            self.assertEqual(self.buy_item_error, result)
