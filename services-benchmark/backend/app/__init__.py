import os
from flask import Flask
from flask_cors import CORS
from .services import mongodb  # Importa il nostro modulo di servizi
from .routes import assignments  # Importa le nostre routes


def create_app():
    """
    Factory per la creazione dell'applicazione Flask.
    """

    # 1. Inizializzazione dell'app Flask
    app = Flask(__name__)

    # 2. Configurazione CORS
    # Abilita CORS per tutte le origini (per i test)
    CORS(app)

    # 3. Connessione ai Servizi (es. MongoDB)
    # Leggiamo l'URI di connessione dalla variabile d'ambiente
    mongo_uri = os.environ.get('MONGO_URI')

    try:
        # Inizializza la connessione al database
        mongodb.init_db(mongo_uri)
        print("Connessione a MongoDB riuscita.")
    except Exception as e:
        print(f"Errore di connessione a MongoDB: {e}")
        # L'app continuerà a girare, ma il DB non sarà connesso

    # 4. Registrazione dei Blueprints (Routes)
    app.register_blueprint(assignments.assignments_bp)

    # (Aggiungeremo altri blueprint qui, es. per le submissions)

    # 5. Endpoint di base (opzionale, lo teniamo qui per ora)
    @app.route('/')
    def hello_world():
        """Endpoint 'Hello World' di base e test connessione DB."""
        db_status = mongodb.check_db_connection()
        return {
            "message": "Hello World! Il server Flask è attivo.",
            "database_status": db_status
        }

    return app
