from flask import Flask
from uuid import uuid4, UUID
from src.config.config import fetch_config

config = fetch_config()
app = Flask(__name__)
app.add_url_rule("/test", endpoint="test")
# set secret key
if config != None:
    app.secret_key = UUID(int=config["secret_key"])
else:
    app.secret_key = uuid4().bytes


@app.endpoint("test")
def session(guid: str):
    return guid


@app.route("/")
def index():
    return "<p>Call endpoint /test</p>"


if __name__ == "__main__" and config != None:
    from waitress import serve

    serve(app, host=config["server"]["host"], port=config["server"]["port"])
