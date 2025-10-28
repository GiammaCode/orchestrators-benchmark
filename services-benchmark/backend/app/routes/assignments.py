import datetime
from flask import Blueprint, request, Response, jsonify
from ..services import mongodb  # Importa le collezioni inizializzate
from ..utils import json_encoder  # Importa l'helper JSON

# 1. Creiamo un Blueprint per raggruppare le rotte
# /api/assignments sarà il prefisso per tutte le rotte in questo file
assignments_bp = Blueprint('assignments_bp', __name__, url_prefix='/api/assignments')


# --- Definizione delle Rotte ---

@assignments_bp.route('', methods=['POST'])
def create_assignment():
    """(Professore) Crea un nuovo compito."""

    # Controlliamo se la collezione è stata inizializzata
    if mongodb.assignments_collection is None:
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

        result = mongodb.assignments_collection.insert_one(new_assignment)

        # Recupera il documento appena creato per restituirlo
        created_doc = mongodb.assignments_collection.find_one({"_id": result.inserted_id})

        return Response(json_encoder.bson_to_json(created_doc), mimetype='application/json'), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@assignments_bp.route('', methods=['GET'])
def get_all_assignments():
    """(Studente/Professore) Restituisce l'elenco di tutti i compiti."""

    if mongodb.assignments_collection is None:
        return jsonify({"error": "Database non connesso"}), 500

    try:
        assignments = list(mongodb.assignments_collection.find({}))
        return Response(json_encoder.bson_to_json(assignments), mimetype='application/json')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
