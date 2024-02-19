from flask import Flask, session, request, json
from werkzeug.exceptions import HTTPException
from uuid import uuid4, UUID
from config.config import fetch_config

config = fetch_config()
app = Flask(__name__)
# set secret key
if config != None:
    app.secret_key = UUID(int=config["secret_key"]).bytes
else:
    app.secret_key = uuid4().bytes


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/add_text", methods=["POST"])
def add_text():
    try:
        if request.method == "POST":
            text = request.json.get("text", None)
            # add text to memory
            error = ""
            if text is None:
                error += f", text: {text}"
            if len(error) != 0:
                raise TypeError(f"invalid type{error}")
            if "text" in session:
                sessionText = session["text"]
                if isinstance(sessionText, list):
                    sessionText.append(text)
                session["text"] = sessionText
            else:
                session["text"] = [text]
            return {"success": True}
        else:
            raise ConnectionRefusedError(f"invalid request method")
    except Exception as exc:
        app.logger.error(exc)
        raise HTTPException(exc)


@app.route("/get_text", methods=["POST"])
def get_text():
    try:
        if request.method == "POST":
            guid = request.json.get("guid", None)
            # return all text pulled from memory/end session
            if isinstance(guid, str):
                if "user" in session and session["user"] == guid:
                    if "text" in session:
                        text = session["text"]
                        session.clear()
                        return {"text": text}
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
        raise HTTPException(exc)


if __name__ == "__main__" and config != None:
    from waitress import serve

    app.debug = True
    serve(app, host=config["server"]["host"], port=config["server"]["port"])
