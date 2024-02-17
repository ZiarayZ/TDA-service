from flask import Flask
from uuid import uuid4, UUID
from src.config.config import fetch_config

config = fetch_config()
app = Flask(__name__)
# set secret key
if config != None:
    app.secret_key = UUID(int=config["secret_key"]).bytes
else:
    app.secret_key = uuid4().bytes

app.add_url_rule("/start_session", endpoint="start_session")
app.add_url_rule("/end_session", endpoint="end_session")


@app.endpoint("start_session")
def start_session():
    sessionId = uuid4()
    return sessionId


@app.endpoint("end_session")
def end_session(guid: str):
    return isinstance(guid, str)


@app.route("/")
def index():
    return "<p>Call endpoint /test</p>"


if __name__ == "__main__" and config != None:
    from waitress import serve

    serve(app, host=config["server"]["host"], port=config["server"]["port"])
