# Step 1: Build React frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ .
RUN npm install && npm run build

# Step 2: Backend con FastAPI + serve React statico
FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Copia backend
COPY backend/ ./backend/
COPY requirements.txt ./

# Copia frontend statico già buildato
COPY --from=frontend-builder /app/frontend/dist ./frontend_dist

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Serve l'app FastAPI + frontend
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
