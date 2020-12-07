# pylint: disable=inconsistent-return-statements
import unittest.mock as mock

def mocked_random_org_call_norm(url, json):
    if (url=="https://api.random.org/json-rpc/2/invoke"
    and json["method"] == "generateIntegerSequences"):
        mocked_call = mock.Mock()
        mocked_call.json.return_value = {
            "result": {
                "random": {
                    "data": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
                }
            }
        }
        return mocked_call

def mocked_local_deck(deck):
    if isinstance(deck, list):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def mocked_call_blackjack(url, json):
    if (url=="https://api.random.org/json-rpc/2/invoke"
    and json["method"] == "generateIntegerSequences"):
        mocked_call = mock.Mock()
        mocked_call.json.return_value = {
            "result": {
                "random": {
                    "data": [[1, 0, 10, 11, 5, 6, 7, 8, 9, 10]]
                }
            }
        }
        return mocked_call

def mocked_bad_deck(url, json):
    if (url=="https://api.random.org/json-rpc/2/invoke"
    and json["method"] == "generateIntegerSequences"):
        mocked_call = mock.Mock()
        mocked_call.json.return_value = {
            "error": "error"
        }
    return mocked_call
