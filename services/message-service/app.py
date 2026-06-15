from flask import Flask, jsonify

app = Flask(__name__)

SERVICE_NAME = "message-service"
VERSION = "v1"
MESSAGE = "Hello from KubeLite v1"


@app.route("/")
def index():
    return jsonify({
        "service": SERVICE_NAME,
        "message": "Message Service is running",
        "version": VERSION
    })


@app.route("/health")
def health():
    return jsonify({
        "service": SERVICE_NAME,
        "status": "healthy"
    })


@app.route("/version")
def version():
    return jsonify({
        "service": SERVICE_NAME,
        "version": VERSION
    })


@app.route("/message")
def message():
    return jsonify({
        "service": SERVICE_NAME,
        "message": MESSAGE,
        "version": VERSION
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)