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