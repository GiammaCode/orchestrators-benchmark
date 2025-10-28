from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Queste variabili sono "globali" all'interno di questo modulo
# Verranno inizializzate da create_app() tramite init_db()
client = None
db = None
assignments_collection = None


# (Aggiungeremo submissions_collection qui)

def init_db(mongo_uri):
    """
    Inizializza la connessione al database e assegna le collezioni.
    """
    global client, db, assignments_collection

    if not mongo_uri:
        print("ATTENZIONE: MONGO_URI non è impostato.")
        raise ValueError("MONGO_URI non è impostato")

    # Tentiamo la connessione
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    # Il comando 'ping' è il modo standard per testare la connessione
    client.admin.command('ping')

    db = client.homework_db  # Il nome del database definito nell'URI
    assignments_collection = db.assignments  # Assegniamo la collezione
    # submissions_collection = db.submissions


def check_db_connection():
    """Controlla lo stato della connessione al DB."""
    if client is None:
        return "Non connesso (client non inizializzato)"
    try:
        client.admin.command('ping')
        return "Connesso"
    except Exception:
        return "Connessione persa"
