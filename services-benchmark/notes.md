# Pagine (Flusso Frontend)
## Homepage (/)
Contiene due link/pulsanti:
- "Area Studenti" (porta a /student)
- "Area Professore" (porta a /professor)

### Pagina Studente (/student)
- Mostra l'elenco di tutti i compiti (assignments) disponibili.
- Per ogni compito, c'è un pulsante "Consegna".
- Cliccando "Consegna", lo studente vede un modulo per caricare i file e inserire:
1) Nome 
2) Cognome 
3) File(s)

### Pagina Professore (/professor)
- Tab 1: Carica Nuovo Compito
Un modulo per creare un nuovo assignment (Titolo, Descrizione, Data Scadenza).

- Tab 2: Vedi Consegne
Mostra un elenco di tutte le consegne (submissions) ricevute per tutti i compiti, ordinate per data.

# Entità (Collezioni MongoDB Semplificate)
## assignments (Compiti)
Memorizza i compiti creati dal professore.
{
  "_id": "ObjectId",
  "title": "string (es. 'Progetto Finale Flask')",
  "description": "string (HTML o Markdown con le istruzioni)",
  "created_at": "ISODate",
  "due_date": "ISODate (scadenza)"
}

## submissions (Consegne)
Memorizza le consegne inviate dagli studenti.
{
  "_id": "ObjectId",
  "assignment_id": "ObjectId (riferimento a `assignments`)",
  "assignment_title": "string (denormalizzato per comodità)",
  "student_name": "string (es. 'Mario Rossi')",
  "submitted_at": "ISODate",
  "files": [
    {
      "filename": "string",
      "url": "string (path su un file storage)"
    }
  ]
}


# Definizione API Endpoints (Flask Semplificati)

## Area Studente
- GET /api/assignments
Azione: (Studente) Restituisce l'elenco di tutti i compiti disponibili.
Risposta: [ { "_id", "title", "description", "due_date" } ]

- GET /api/assignments/<assignment_id>
Azione: (Studente) Restituisce i dettagli di un singolo compito.
Risposta: { "_id", "title", "description", "due_date" }

POST /api/assignments/<assignment_id>/submit
Azione: (Studente) Invia una consegna per un compito.
Payload: (multipart/form-data)
student_name (string)
files (uno o più file)
Risposta: { ... (dettagli nuova consegna) }

## Area Professore
- POST /api/assignments
Azione: (Professore) Crea un nuovo compito.
Payload (JSON): { "title", "description", "due_date" }
Risposta: { ... (dettagli nuovo compito) }

- GET /api/submissions
Azione: (Professore) Restituisce l'elenco di tutte le consegne ricevute.
Risposta: [ { "_id", "assignment_title", "student_name", "submitted_at", "files": [...] } ]

- GET /api/submissions/<submission_id>
Azione: (Professore) Restituisce i dettagli di una singola consegna.
Risposta: [ { "_id", "assignment_title", "student_name", "submitted_at", "files": [...] } ]

_________________________________________________________________________________________________________

# Piano di Sviluppo (Milestones)

## Milestone 1: Setup Ambiente (Docker & Flask)

Obiettivo: Creare un ambiente di sviluppo containerizzato funzionante.

- docker-compose.yml:
- Definire due servizi: backend (la nostra app Flask) e db (l'immagine ufficiale di mongo).
- Configurare i volumi per il database (per la persistenza) e per il codice backend (per il live-reloading).
- Impostare le variabili d'ambiente (es. MONGO_URI).
- Dockerfile (per il backend):
- Partire da un'immagine Python ufficiale (es. python:3.10-slim).
- Creare una directory di lavoro. 
- Installare le dipendenze da requirements.txt. 
- Definire il comando di avvio (es. flask run --host=0.0.0.0). 
- requirements.txt:
- Aggiungere le librerie base: Flask, pymongo, python-dotenv, Flask-Cors (essenziale per il frontend). 
- Struttura App Iniziale:
- Creare un app.py di base che si connette a MongoDB e restituisce un JSON di "hello world" su /api.

## Milestone 2: Backend - API Core (Gestione Compiti)
Obiettivo: Implementare gli endpoint per creare e visualizzare i compiti.
- Connessione a MongoDB:
- Configurare pymongo in Flask per connettersi al servizio db. 
- Gestire correttamente gli ObjectId di BSON. 
- Endpoint Professore (Creazione):
- POST /api/assignments: Implementare la logica per ricevere il JSON (title, description, due_date), validarlo e inserirlo nella collezione assignments. 
- Endpoint Studente (Lettura):
- GET /api/assignments: Implementare la logica per recuperare tutti i compiti dalla collezione. 
- GET /api/assignments/<assignment_id>: Implementare la logica per recuperare un singolo compito.

## Milestone 3: Backend - API File Upload (Gestione Consegne)
Obiettivo: Implementare la logica di upload dei file e la creazione delle consegne.

- Configurazione Uploads:
- Creare una cartella (es. ./uploads) che sarà mappata come volume in Docker. 
- Configurare Flask per gestire i file in arrivo (usando request.files). 
- Endpoint Studente (Invio):
- POST /api/assignments/<assignment_id>/submit:
- Recuperare il student_name da request.form. 
- Ciclare su request.files.getlist('files') per salvare ogni file sul disco (con un nome univoco). 
- Creare il documento submission nel database, includendo i metadati dei file (nome, path/url). 
- Endpoint Professore (Lettura Consegne):
- GET /api/submissions: Recuperare tutte le consegne. 
- GET /api/submissions/<submission_id>: Recuperare una singola consegna. 
- Endpoint Servizio File:
- Creare un endpoint GET /uploads/<filename> che serve i file statici dalla cartella di upload (necessario per farli scaricare al professore).

## Milestone 4: Frontend - Struttura e Pagina Professore
Obiettivo: Creare l'interfaccia statica (HTML/CSS) e la logica per il professore.

- index.html (Single Page Application):
- Creare un unico file HTML.
- Usare JavaScript per mostrare/nascondere le diverse "pagine" (Homepage, Studente, Professore).
- Styling base con Tailwind CSS (o CSS semplice).

Homepage:
Creare i due pulsanti "Area Studente" e "Area Professore".
Pagina Professore (UI):
Implementare il layout a Tab.
Tab 1 (Crea Compito): Creare il form HTML (title, description, due_date).
Tab 2 (Vedi Consegne): Creare un contenitore vuoto per l'elenco.
Logica Professore (JS):
Collegare il form (Tab 1) alla POST /api/assignments usando fetch().
Al caricamento della pagina, chiamare GET /api/submissions e popolare dinamicamente il Tab 2.

## Milestone 5: Frontend - Pagina Studente e Interattività
Obiettivo: Completare il flusso per lo studente.
Pagina Studente (UI):
Creare un contenitore per l'elenco dei compiti.
Creare un modale/sezione nascosta per il form di consegna (Nome, Cognome, Input File multiple).
Logica Studente (JS):
Al caricamento della pagina, chiamare GET /api/assignments e popolare l'elenco.
Gestire il click sul pulsante "Consegna" per mostrare il form e passare l'assignment_id.
Gestire l'invio del form (usando FormData per l'upload multipart) verso POST /api/assignments/<assignment_id>/submit.

## Milestone 6: Testing e Refinement
Obiettivo: Assicurarsi che tutto funzioni end-to-end.
Test E2E:
Professore crea compito -> Studente vede compito -> Studente invia consegna -> Professore vede consegna e scarica i file.
Gestione Errori:
Assicurarsi che il frontend mostri messaggi d'errore (es. "Upload fallito", "Compito non trovato").
Styling:
Rifinire il CSS per rendere l'applicazione utilizzabile.