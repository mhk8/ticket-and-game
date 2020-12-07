from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = getenv("SECRET_KEY", "DEFAULT_KEY")

    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = "filesystem"

    TEMPLATE_FOLDER = "../build"
    STATIC_FOLDER = "../build/static"
