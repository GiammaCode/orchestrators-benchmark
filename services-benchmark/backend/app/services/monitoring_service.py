import os
from datetime import datetime
from app.extensions import mongo
from config import Config


def check_health():
    """
     Retrieves connectivity to MongoDB and storage volume accessibility.
    """
    health_status = {}
    # check the ping with MongoDB
    try:
        mongo.db.command('ping')
        health_status['mongodb'] = 'connected'
    except Exception:
        health_status['mongodb'] = 'error'

    # check volumes accessibility
    try:
        volume_ok = Config.UPLOAD_DIR.exists() and os.access(Config.UPLOAD_DIR, os.W_OK)
        health_status['volume'] = 'accesible'
    except Exception:
        health_status['volume'] = 'error'

    return health_status


def get_application_stats():
    """
        Calculate and return application statistics.
    """
    db = mongo.db

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    hour_start = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

    # does query
    total_today = db.submissions.count_documents({"timestamp": {"$gte": today_start}})
    total_hour = db.submissions.count_documents({"timestamp": {"$gte": hour_start}})
    total_submissions = db.submissions.count_documents({})

    # Aggregation for assigment
    pipeline = [
        {"$group": {"_id": "$assignment_id", "count": {"$sum": 1}}}
    ]
    per_assignment = {item["_id"]: item["count"] for item in db.submissions.aggregate(pipeline)}

    return {
        "submissions_today": total_today,
        "submissions_last_hour": total_hour,
        "total_submissions": total_submissions,
        "submissions_per_assignment": per_assignment
    }


