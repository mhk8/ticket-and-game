# pylint: disable=ungrouped-imports
# pylint: disable=unused-import
# pylint: disable=invalid-name
# pylint: disable=unused-argument
from server.routes.leaderboard import get_leader_board
import unittest
import os
import sys
import unittest.mock as mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


db_session = UnifiedAlchemyMagicMock()

LEADERBOARD_DATA = [
    (1, "Jack", 180),
    (2, "James", 80),
    (3, "Sally", 50),
]


def returnMockData(*_args, **_kwargs):
    mocked_query_user = mock.Mock()
    mocked_query_user.outerjoin().group_by().order_by().all.return_value = (
        LEADERBOARD_DATA
    )
    return mocked_query_user


class LeaderboardTest(unittest.TestCase):
    def test_success_leaderboard(self):
        with mock.patch("server.db.session.query", returnMockData):
            response = get_leader_board()

            self.assertIs(type(response), dict)

            mocked_data = LEADERBOARD_DATA

            for i, transaction in enumerate(response["transactions"]):
                row = LEADERBOARD_DATA[i]
                self.assertEqual(transaction["id"], row[0])
                self.assertEqual(transaction["name"], row[1])
                self.assertEqual(transaction["balance"], row[2])
