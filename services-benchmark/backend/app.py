import os
import datetime
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from bson.json_util import dumps, loads

app = Flask(__name__)
CORS(app)

# connect to mongodb
mongo_uri = os.environ.get('MONGO_URI')
client = None
db = None
assigment_collection = None

if not mongo_uri:
    print("Error, mongoDB failed")
else:
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # test connection
        client.admin.command('ping')
        print("MongoDB connection established")
        db = client.submission_management_db  # database name defined in the URI
        assignments_collection = db.assignments  # Assegniamo la collezione
    except ConnectionFailure as e:
        print(f"Error, MongoDB connection failed: {e}")

# 4. Helper per la serializzazione BSON
def bson_to_json(data):
    """Converte dati BSON (come ObjectId e ISODate) in stringhe JSON."""
    return dumps(data)

@app.route('/')
def hello_world():
    """Endpoint 'Hello World' di base e test connessione DB."""
    db_status = "Non connesso"
    if client is not None:
        try:
            # Facciamo un ping per essere sicuri che la connessione sia ancora attiva
            client.admin.command('ping')
            db_status = "Connesso"
        except Exception:
            db_status = "Connessione persa"

    return jsonify({
        "message": "Hello World! Il server Flask è attivo.",
        "database_status": db_status
    })


@app.route('/api/assignments', methods=['POST'])
def create_assignment():
    """(Professore) Crea un nuovo compito."""
    if not db:
        return jsonify({"error": "Database non connesso"}), 500

    try:
        data = request.json
        if not data or 'title' not in data:
            return jsonify({"error": "Titolo mancante"}), 400

        new_assignment = {
            "title": data.get('title'),
            "description": data.get('description', ''),
            "due_date": data.get('due_date'),  # Assumiamo formato ISO
            "created_at": datetime.datetime.now(datetime.timezone.utc)
        }

        result = assignments_collection.insert_one(new_assignment)

        # Recupera il documento appena creato per restituirlo
        created_doc = assignments_collection.find_one({"_id": result.inserted_id})

        # Usiamo Response e l'helper bson_to_json per gestire ObjectId
        return Response(bson_to_json(created_doc), mimetype='application/json'), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/assignments', methods=['GET'])
def get_all_assignments():
    """(Studente/Professore) Restituisce l'elenco di tutti i compiti."""
    if db is None:  # CORREZIONE: Cambiato 'if not db:'
        return jsonify({"error": "Database non connesso"}), 500

    try:
        assignments = list(assignments_collection.find({}))
        # Usiamo Response e l'helper bson_to_json
        return Response(bson_to_json(assignments), mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Avvio del server ---

if __name__ == '__main__':
    # Flask userà le variabili d'ambiente FLASK_RUN_HOST e FLASK_DEBUG
    # definite nel docker-compose.yml
    app.run()


