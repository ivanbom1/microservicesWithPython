# logging-service — Flask app (not FastAPI — intentional, see docs/specs.md)
#
# Run with:   flask run --port 8006
# Or:         python -m flask --app app.main run --port 8006
#
# YOUR TASK: implement the four consent endpoints and the log deletion endpoint.
# The response shapes are in docs/api-contracts.md.

import os
import threading

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from datetime import datetime, timezone

from app.models import ActivityLog, Consent, db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///./logging.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # Start the RabbitMQ consumer in a background thread
    from app.consumer import start_consumer
    threading.Thread(target=start_consumer, args=(app,), daemon=True).start()


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "logging-service"})


# ---------------------------------------------------------------------------
# YOUR TASK — implement the five endpoints below
# ---------------------------------------------------------------------------

@app.post("/v1/consent/<user_id>")
def set_consent(user_id):
    """1. Parse request.get_json() to get "granted" (bool)"""
    data = request.get_json()
    granted = data["granted"]
    """2. Look up or create a Consent row for user_id"""
    consent = Consent.query.filter_by(user_id=user_id).first()
    if not consent:
        consent = Consent(user_id=user_id)
        db.session.add(consent)
    """3. Set granted and updated_at, then db.session.commit()"""
    consent.granted = granted
    consent.updated_at = datetime.utcnow()
    db.session.commit()
    """ 4. Return 200 with { "user_id", "granted", "updated_at" }"""
    return jsonify({
        "user_id": user_id,
        "granted": consent.granted,
        "updated_at": consent.updated_at.isoformat()
    }), 200


@app.get("/v1/consent/<user_id>")
def get_consent(user_id):
    """
    Check a user's current consent status.

    Steps:
    1. Query Consent by user_id
    2. If not found → 404 with { "detail": "No consent record found" }
    3. Otherwise → 200 with { "user_id", "granted", "updated_at" }
    """
    consent = Consent.query.filter_by(user_id=user_id).first()
    if consent:
        return jsonify({
        "user_id": user_id,
        "granted": consent.granted,
        "updated_at": consent.updated_at.isoformat()
    }), 200
    else:
        return jsonify({
            "detail": "No consent record found"
        }), 404



@app.delete("/v1/consent/<user_id>")
def withdraw_consent(user_id):
    """
    Withdraw consent — sets granted to False (does not delete the record).

    Steps:
    1. Look up the Consent row; 404 if missing
    2. Set granted=False, update updated_at, commit
    3. Return 200 with { "user_id", "granted", "updated_at" }
    """
    consent = Consent.query.filter_by(user_id=user_id).first()
    if consent:
        consent.granted = False
        consent.updated_at = datetime.utcnow()
        db.session.commit()
    else:
        return jsonify({
            "detail": "No consent record found"
        }), 404


@app.delete("/v1/logs/<user_id>")
def delete_logs(user_id):
    """
    GDPR right to erasure — permanently delete all log entries for a user.

    Steps:
    1. Delete all ActivityLog rows where user_id matches
    2. Commit
    3. Return 200 with { "user_id", "deleted_entries": <count> }
    """
    logs = ActivityLog.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    if logs:
        return jsonify({
            "user_id": user_id,
            "deleted_entries": logs
        }), 200
    else:
        return jsonify({
            "detail": "Activity logs are not found"
        }), 404


@app.get("/v1/logs/<user_id>")
def get_logs(user_id):
    logs = ActivityLog.query.filter_by(user_id=user_id).all()

    return jsonify({
        "items": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "game_id": log.game_id,
                "action": log.action,
                "message": log.message,
                "created_at": log.created_at.isoformat() #serializes the datetime 
            }
            for log in logs
        ],
        "total": len(logs)
    }), 200
