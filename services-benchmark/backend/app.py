import os
import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
CORS(app)

# connect to mongodb
mongo_uri = os.environ.get('MONGO_URI')
client = None
db = None

if not mongo_uri:
    print("Error, mongoDB failed")
else:
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # test connection
        client.admin.command('ping')
        print("MongoDB connection established")
        db = client.submission_management_db  # database name defined in the URI
    except ConnectionFailure as e:
        print(f"Error, MongoDB connection failed: {e}")


@app.route('/')
def hello_world():
    db_status = "Not connected"
    if client is not None:
        try:
            # Facciamo un ping per essere sicuri che la connessione sia ancora attiva
            client.admin.command('ping')
            db_status = "Connected"
        except Exception:
            db_status = "Connection lost"

    return jsonify({
        "message": "Hello World! Il server Flask è attivo.",
        "database_status": db_status
    })


# ==================================================
# == Altri Endpoints (da aggiungere)
# ==================================================

# ... (Aggiungeremo /api/assignments, /api/submissions, ecc. qui)

# --- Avvio del server ---

if __name__ == '__main__':
    # Flask userà le variabili d'ambiente FLASK_RUN_HOST e FLASK_DEBUG
    # definite nel docker-compose.yml
    app.run()
