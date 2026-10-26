import json
from pathlib import Path
from threading import Lock

from flask import Flask, request, jsonify

app = Flask(__name__)
DATA_FILE = Path(__file__).resolve().parent / "data.json"
DATA_LOCK = Lock()
REQUIRED_FIELDS = ("name", "email", "message")


@app.route("/")
def home():
    return "Flask app is working"


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    cleaned_data = {}
    for field in REQUIRED_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return jsonify({"error": f"A valid {field} is required."}), 400
        cleaned_data[field] = value.strip()

    with DATA_LOCK:
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []
        except json.JSONDecodeError:
            app.logger.exception("Stored submissions file contains invalid JSON.")
            return jsonify({"error": "Stored submissions could not be read."}), 500
        except OSError:
            app.logger.exception("Could not read stored submissions.")
            return jsonify({"error": "Stored submissions could not be read."}), 500

        if not isinstance(existing_data, list):
            app.logger.error("Stored submissions file must contain a JSON array.")
            return jsonify({"error": "Stored submissions could not be read."}), 500

        existing_data.append(cleaned_data)

        try:
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4, ensure_ascii=False)
                file.write("\n")
        except OSError:
            app.logger.exception("Could not save submission.")
            return jsonify({"error": "Submission could not be saved."}), 500

    return jsonify({"message": "Form submitted  jfjfj successfully!"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)