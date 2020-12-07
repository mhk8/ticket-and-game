import server.models as table
import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


KEY_INPUT = "input"
KEY_EXPECTED = "expected"


class SqlEnumTest(unittest.TestCase):
    def setUp(self):
        self.success_test_params_user = [
            {KEY_INPUT: "google", KEY_EXPECTED: "GOOGLE"},
            {KEY_INPUT: "password", KEY_EXPECTED: "PASSWORD"},
        ]
        self.success_test_params_transaction = [
            {KEY_INPUT: "transfer", KEY_EXPECTED: "TRANSFER"},
            {KEY_INPUT: "coinfilp", KEY_EXPECTED: "COINFILP"},
        ]

    def test_success_login_type(self):
        for test_case in self.success_test_params_user:
            result = table.user.LoginType(test_case[KEY_INPUT]).name
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(expected, result)

    def test_success_activity_type(self):
        for test_case in self.success_test_params_transaction:
            result = table.transaction.ActivityType(test_case[KEY_INPUT]).name
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(expected, result)
