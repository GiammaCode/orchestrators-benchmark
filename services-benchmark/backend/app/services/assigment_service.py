from datetime import datetime
from bson.objectid import ObjectId
from app.extensions import mongo


def create_assignment(data):
    """
    Manages business logic to create a new assignment.
    """
    required_fields = ['course_id', 'title', 'deadline', 'max_file_size']
    if not all(field in data for field in required_fields):
        raise ValueError("Missing required fields")

    try:
        # Converte la stringa ISO in un oggetto datetime consapevole del fuso orario
        deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
    except (ValueError, TypeError):
        raise ValueError("Invalid deadline format. Use ISO 8601 format.")

    assignment_data = {
        "course_id": data['course_id'],
        "title": data['title'],
        "deadline": deadline,
        "max_file_size": data['max_file_size'],
        "created_at": datetime.utcnow()
    }

    result = mongo.db.assignments.insert_one(assignment_data)
    return str(result.inserted_id)


def get_active_assignments():
    """
    Retrieves all active assignments, with an open deadline.
    """
    now = datetime.utcnow()
    assignments_cursor = mongo.db.assignments.find(
        {"deadline": {"$gte": now}}
    ).sort("deadline", 1)

    assignments = []
    for assign in assignments_cursor:
        assign["assignment_id"] = str(assign.pop("_id"))
        assign["deadline"] = assign["deadline"].isoformat()
        assign["created_at"] = assign["created_at"].isoformat()
        assignments.append(assign)

    return assignments


def get_assignment_details(assignment_id):
    """
    Retrieves details about a specific assignment, within submissions-count.
    """
    try:
        obj_id = ObjectId(assignment_id)
    except Exception:
        return None

    assignment = mongo.db.assignments.find_one({"_id": obj_id})
    if not assignment:
        return None

    # Counts submissions
    submission_count = mongo.db.submissions.count_documents({
        "assignment_id": assignment_id
    })

    assignment["assignment_id"] = str(assignment.pop("_id"))
    assignment["deadline"] = assignment["deadline"].isoformat()
    assignment["created_at"] = assignment["created_at"].isoformat()
    assignment["submission_count"] = submission_count

    return assignment