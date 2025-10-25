# 1. Image de base Python 3.10 légère
FROM python:3.10-slim

# 2. Définir le dossier de travail
WORKDIR /app

# 3. Copier les fichiers du projet
COPY . /app

# 4. Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

# 5. Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Exposer le port utilisé par Hugging Face (généralement 7860 ou 8000)
EXPOSE 7860

# 7. Démarrer le serveur FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]


