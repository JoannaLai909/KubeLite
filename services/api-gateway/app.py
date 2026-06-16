from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

SERVICE_NAME = "api-gateway"
VERSION = "v1"


@app.route("/")
def index():
    return jsonify({
        "service": SERVICE_NAME,
        "message": "KubeLite API Gateway is running",
        "version": VERSION
    })


@app.route("/health")
def health():
    return jsonify({
        "service": SERVICE_NAME,
        "status": "healthy",
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()

    })


@app.route("/version")
def version():
    return jsonify({
        "service": SERVICE_NAME,
        "version": VERSION
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)