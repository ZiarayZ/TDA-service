from flask import Flask, session, request
from uuid import uuid4, UUID
from src.config.config import fetch_config

config = fetch_config()
app = Flask(__name__)
# set secret key
if config != None:
    app.secret_key = UUID(int=config["secret_key"]).bytes
else:
    app.secret_key = uuid4().bytes


@app.route("/start_session", methods=["POST"])
def start_session():
    try:
        if request.method == "POST":
            sessionId = uuid4().hex
            session["user"] = sessionId
            # request memory/start session
            return {"guid": sessionId}
        else:
            raise ConnectionRefusedError("invalid request method")
    except Exception as exc:
        app.logger.error(exc)


@app.route("/add_text", methods=["POST"])
def add_text():
    try:
        if request.method == "POST":
            guid = request.json.get("guid", None)
            text = request.json.get("text", None)
            # add text to memory
            if isinstance(guid, str) and isinstance(text, str):
                if "user" in session and session["user"] == guid:
                    return {"guid": guid, "text": text}
                else:
                    app.logger.debug(f"invalid user: {guid}")
            else:
                app.logger.warning(f"invalid type, user: {guid}, text: {text}")
            # FIXME: return possible exceptions that Jira or Slack can handle
        else:
            raise ConnectionRefusedError(f"invalid request method")
    except Exception as exc:
        app.logger.error(exc)


@app.route("/end_session", methods=["POST"])
def end_session():
    try:
        if request.method == "POST":
            guid = request.json.get("guid", None)
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
        else:
            raise ConnectionRefusedError("invalid request method")
    except Exception as exc:
        app.logger.error(exc)


@app.route("/")
def index():
    return "<p>Call endpoint /start_session</p><p>Call endpoint /add_text as many times as needed</p><p>Call endpoint /end_session</p>"


if __name__ == "__main__" and config != None:
    from waitress import serve

    serve(app, host=config["server"]["host"], port=config["server"]["port"])
