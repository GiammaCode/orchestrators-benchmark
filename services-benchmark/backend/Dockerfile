# Usiamo un'immagine Python ufficiale
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Usiamo "flask run" che rileva FLASK_APP, FLASK_DEBUG e FLASK_RUN_HOST dalle env vars
CMD ["flask", "run"]
