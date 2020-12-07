import unittest
from unittest import mock

from server import create_app
from config import Config


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config())
        self.client = self.app.test_client()

    def test_index_endpoint(self):
        with mock.patch(
            "server.routes.send_from_directory", lambda _dir, _name: ({}, 200)
        ):
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)

        with mock.patch(
            "server.routes.send_from_directory", lambda _dir, _name: ({}, 200)
        ):
            response = self.client.get("/a/directory/that/should/not/exist")
            self.assertEqual(response.status_code, 200)
