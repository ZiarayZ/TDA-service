from flask import Flask
from werkzeug.exceptions import HTTPException
from uuid import uuid4, UUID
from src.config.config import fetch_config
from src.flask import error, append

config = fetch_config()
app = Flask(__name__)
# set secret key
if config != None:
    app.secret_key = UUID(int=config["secret_key"]).bytes
else:
    app.secret_key = uuid4().bytes


@app.errorhandler(HTTPException)
def errorHandler(e):
    app.logger.error(e)
    return error.handle_exception(e)


@app.route("/add_text", methods=["POST"])
def add_text():
    try:
        return append.handle_text()
    except Exception as exc:
        raise HTTPException(exc)


@app.route("/get_text", methods=["POST"])
def get_text():
    try:
        return append.handle_return()
    except Exception as exc:
        raise HTTPException(exc)


if __name__ == "__main__" and config != None:
    from waitress import serve

    app.debug = True
    serve(app, host=config["server"]["host"], port=config["server"]["port"])
