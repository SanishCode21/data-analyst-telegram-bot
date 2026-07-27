from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Telegram Data Analyst Bot is running......"


@app.route("/health")
def health():
    return {"status": "ok"}


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


