from flask import Flask
from src.config.config import fetch_config

config = fetch_config()
app = Flask(__name__)
app.add_url_rule("/test", endpoint="test")


@app.endpoint("test")
def session():
    return ""


@app.route("/")
def index():
    return "<p>Call endpoint /test</p>"
