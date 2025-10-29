import os
from flask import Flask
from flask_cors import CORS
from .services import mongodb
from .routes import assignments


def create_app():
    """
    Flask app factory, to create the application.
    """
    app = Flask(__name__)
    CORS(app)
    mongo_uri = os.environ.get('MONGO_URI')
    try:
        mongodb.init_db(mongo_uri)
        print("MongoDB connected with successfully")
    except Exception as e:
        print(f"MongoDB connection error: {e}")

    app.register_blueprint(assignments.assignments_bp)
    # TO DO, new blueprint per le submissions

    @app.route('/')
    def hello_world():
        """Base endpoint for testing purposes (DB connection)) ."""
        db_status = mongodb.check_db_connection()
        return {
            "message": "Hello World! Flask server is alive.",
            "database_status": db_status
        }

    return app
