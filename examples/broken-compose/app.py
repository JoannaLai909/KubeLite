import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    db_url = os.getenv("DATABASE_URL", "")
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        return "OK"
    except Exception as e:
        return f"DB Error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
