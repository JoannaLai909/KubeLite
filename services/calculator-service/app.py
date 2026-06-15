from flask import Flask, jsonify, request

app = Flask(__name__)

SERVICE_NAME = "calculator-service"
VERSION = "v1"


@app.route("/")
def index():
    return jsonify({
        "service": SERVICE_NAME,
        "message": "Calculator Service is running",
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


@app.route("/add")
def add():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))

        return jsonify({
            "service": SERVICE_NAME,
            "operation": "add",
            "a": a,
            "b": b,
            "result": a + b
        })

    except ValueError:
        return jsonify({
            "service": SERVICE_NAME,
            "error": "Invalid input. Please provide numbers for a and b."
        }), 400


@app.route("/multiply")
def multiply():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))

        return jsonify({
            "service": SERVICE_NAME,
            "operation": "multiply",
            "a": a,
            "b": b,
            "result": a * b
        })

    except ValueError:
        return jsonify({
            "service": SERVICE_NAME,
            "error": "Invalid input. Please provide numbers for a and b."
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)