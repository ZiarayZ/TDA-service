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
            guid = request.json.get("guid", None)
            if isinstance(guid, str) is False:
                guid = uuid4().hex  # generate one for them
            sessionId = session["user"]
            if sessionId == guid:
                guid = uuid4().hex  # duplicate guid try again
            session["user"] = guid
            session["text"] = []
            # request memory/start session
            return {"guid": guid}
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
            error = ""
            if isinstance(guid, str) is False:
                error += f", user: {guid}"
            if text is None:
                error += f", text: {text}"
            if len(error) != 0:
                raise TypeError(f"invalid type{error}")

            if "user" in session and session["user"] == guid:
                if "text" in session:
                    sessionText = session["text"]
                    if isinstance(sessionText, list):
                        sessionText.append(text)
                    session["text"] = sessionText
                else:
                    session["text"] = [text]
                return {"text": text}
            else:
                raise IndexError(f"invalid user: {guid}")
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
                    if "text" in session:
                        session.clear()
                        return {"text": session["text"]}
                    else:
                        raise IndexError("missing text")
                else:
                    raise IndexError(f"invalid user: {guid}")
            else:
                raise TypeError(f"invalid type, user: {guid}")
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
