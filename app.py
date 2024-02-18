from flask import Flask, session
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
app.add_url_rule("/add_text", endpoint="add_text")
app.add_url_rule("/end_session", endpoint="end_session")


@app.endpoint("start_session")
def start_session():
    sessionId = uuid4().hex
    session["user"] = sessionId
    # request memory/start session
    return sessionId


@app.endpoint("add_text")
def add_text(guid: str, text: str):
    # add text to memory
    if isinstance(guid, str) and isinstance(text, str):
        if "user" in session and session["user"] == guid:
            return guid
        else:
            app.logger.debug(f"invalid user: {guid}")
    else:
        app.logger.warning(f"invalid type, user: {guid}, text: {text}")
    # FIXME: return possible exceptions that Jira or Slack can handle


@app.endpoint("end_session")
def end_session(guid: str):
    # return all text pulled from memory/end session
    if isinstance(guid, str):
        if "user" in session and session["user"] == guid:
            session.pop("user")
            return True
        else:
            app.logger.debug(f"invalid user: {guid}")
    else:
        app.logger.warning(f"invalid type, user: {guid}")
    # FIXME: return possible exceptions that Jira or Slack can handle


@app.route("/")
def index():
    return "<p>Call endpoint /start_session</p><p>Call endpoint /add_text as many times as needed</p><p>Call endpoint /end_session</p>"


if __name__ == "__main__" and config != None:
    from waitress import serve

    serve(app, host=config["server"]["host"], port=config["server"]["port"])
