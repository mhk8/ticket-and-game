from unittest import TestCase

from server import db, create_app
from config import Config


class DatabaseTest(TestCase):
    def setUp(self):
        config = Config()
        config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        self.app = create_app(config)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            db.session.commit()
