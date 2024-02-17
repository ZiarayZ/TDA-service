from flask import Flask
from src.config.config import fetch_config

config = fetch_config()
app = Flask(__name__)
app.add_url_rule("/test", endpoint="test")


@app.endpoint("test")
def session(guid: str):
    return guid


@app.route("/")
def index():
    return "<p>Call endpoint /test</p>"


if __name__ == "__main__" and config != None:
    from waitress import serve

    serve(app, host=config["server"]["host"], port=config["server"]["port"])
