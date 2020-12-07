from unittest import TestCase

from server import db
from server.utils.database_test import DatabaseTest
from server.models import Store


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_ID = "id"
KEY_NAME = "name"
KEY_ITEM_GROUP = "item_group"
KEY_GROUP = "group"
KEY_LIMIT = "limit"
KEY_ITEMS = "items"
KEY_PRICE = "price"


class StoreListTest(DatabaseTest):
    def setUp(self):
        super().setUp()

        self.list_test_cases = [
            {
                KEY_INPUT: {
                    KEY_ID: 111,
                    KEY_NAME: "test",
                    KEY_ITEM_GROUP: 1,
                    KEY_LIMIT: 1,
                    KEY_PRICE: 123,
                },
                KEY_EXPECTED: {
                    KEY_ID: 111,
                    KEY_NAME: "test",
                    KEY_GROUP: 1,
                    KEY_LIMIT: 1,
                    KEY_PRICE: 123,
                },
            },
            {
                KEY_INPUT: {
                    KEY_ID: 33333,
                    KEY_NAME: "item name",
                    KEY_ITEM_GROUP: 1,
                    KEY_LIMIT: 1,
                    KEY_PRICE: 123,
                },
                KEY_EXPECTED: {
                    KEY_ID: 33333,
                    KEY_NAME: "item name",
                    KEY_GROUP: 1,
                    KEY_LIMIT: 1,
                    KEY_PRICE: 123,
                },
            },
            {
                KEY_INPUT: {
                    KEY_ID: 1,
                    KEY_NAME: "test",
                    KEY_ITEM_GROUP: 1,
                    KEY_LIMIT: 1,
                    KEY_PRICE: 123,
                },
                KEY_EXPECTED: {
                    KEY_ID: 1,
                    KEY_NAME: "test",
                    KEY_GROUP: 1,
                    KEY_LIMIT: 1,
                    KEY_PRICE: 123,
                },
            },
        ]

    def test_list(self):
        with self.app.app_context():
            with self.client.session_transaction() as sess:
                sess["user_id"] = 1
            for test_case in self.list_test_cases:
                item = Store(**test_case[KEY_INPUT])
                db.session.add(item)
                db.session.commit()

                item_id = test_case[KEY_INPUT][KEY_ID]

                response = self.client.get("/api/store/list").json

                response_item = None
                for returned_item in response[KEY_ITEMS]:
                    if returned_item[KEY_ID] == item_id:
                        response_item = returned_item
                        break

                self.assertDictEqual(test_case[KEY_EXPECTED], response_item)
