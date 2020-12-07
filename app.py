from os import getenv

from server import create_app

from config import Config

config = Config()
app = create_app(config)

if __name__ == "__main__":
    app.run(
        host=getenv("IP", "0.0.0.0"),
        port=int(getenv("PORT", "80")),
        debug=getenv("DEBUG", False),
    )
