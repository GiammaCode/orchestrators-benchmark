# frontend/Dockerfile

# Usa un'immagine Node ufficiale leggera
FROM node:18-alpine

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia i file di configurazione delle dipendenze
COPY package*.json ./

# Installa le dipendenze
RUN npm install

# Copia tutto il resto del codice sorgente
COPY . .

# Espone la porta 3000 (default di React)
EXPOSE 3000

# Avvia l'applicazione in modalità sviluppo
CMD ["npm", "start"]