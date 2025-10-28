from app import create_app # Importa la factory dal package 'app' (la cartella backend)

# 1. Crea l'istanza dell'app chiamando la factory
# Leggerà automaticamente le variabili d'ambiente
app = create_app()

# 2. Avvio del server
if __name__ == '__main__':
    # Flask userà le variabili d'ambiente FLASK_RUN_HOST e FLASK_DEBUG
    # definite nel docker-compose.yml
    app.run()

