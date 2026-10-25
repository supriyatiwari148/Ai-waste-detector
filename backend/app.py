"""Flask API for the AI Waste Sorting Assistant."""
import logging
import os

from dotenv import load_dotenv

load_dotenv()  # must run BEFORE importing modules that read environment variables

from flask import Flask, jsonify, request  # noqa: E402
from flask_cors import CORS  # noqa: E402

import classifier  # noqa: E402
import database  # noqa: E402
from disposal_guidance import get_guidance  # noqa: E402

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("waste-api")

ALLOWED_EXT = {"jpg", "jpeg", "png"}
MAX_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_MB * 1024 * 1024  # Flask rejects bigger bodies (413)

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
CORS(app, resources={r"/api/*": {"origins": origins}})

database.init_db()

DISCLAIMER = (
    "Confidence is the model's own estimate, not a guarantee of accuracy. "
    "The AI matches your photo to a list of common waste items and can be wrong, "
    "especially on unusual, dirty or mixed items. Rules differ by city."
)


def error(message, status):
    return jsonify({"success": False, "error": message}), status


@app.get("/")
def status():
    return jsonify({"success": True, "service": "AI Waste Sorting Assistant API",
                    "model": classifier.MODEL_ID, "model_loaded": classifier.is_loaded()})


@app.post("/api/classify")
def classify_route():
    file = request.files.get("image")
    if file is None or file.filename == "":
        return error("No image uploaded. Send a file in the 'image' field.", 400)

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXT:
        return error("Only JPG, JPEG and PNG images are allowed.", 400)

    data = file.read()  # kept in memory only; never written to disk
    try:
        result = classifier.classify(data)
    except classifier.InvalidImageError as exc:
        return error(str(exc), 400)
    except classifier.ModelUnavailableError:
        return error("The AI model is not available right now. Please try again later.", 503)
    except Exception:  # noqa: BLE001
        log.exception("Unexpected classification error")
        return error("Something went wrong while analysing the image.", 500)

    guidance = get_guidance(result["label"], uncertain=result["uncertain"])
    entry_id = database.add_entry(
        result["label"], guidance["title"], result["confidence"], result["uncertain"]
    )
    return jsonify({"success": True, "id": entry_id, **result,
                    "category": guidance["title"], "guidance": guidance, "disclaimer": DISCLAIMER})


@app.get("/api/history")
def history_get():
    return jsonify({"success": True, "history": database.list_entries()})


@app.delete("/api/history")
def history_delete():
    database.clear_entries()
    return jsonify({"success": True})


@app.post("/api/feedback")
def feedback():
    body = request.get_json(silent=True) or {}
    entry_id, correct = body.get("id"), body.get("correct")
    if not isinstance(entry_id, int) or not isinstance(correct, bool):
        return error("Send JSON like {\"id\": 1, \"correct\": true}.", 400)
    if not database.set_feedback(entry_id, correct):
        return error("History entry not found.", 404)
    return jsonify({"success": True})


@app.errorhandler(413)
def too_large(_):
    return error(f"File is too large. Maximum size is {MAX_MB} MB.", 413)


@app.errorhandler(404)
def not_found(_):
    return error("Route not found.", 404)


@app.errorhandler(500)
def server_error(_):
    return error("Internal server error.", 500)


if __name__ == "__main__":
    # Development server (debug OFF). For production use: waitress-serve --port=5000 app:app
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
