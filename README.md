# utilisateur-avec-react-vite-et-django-et-postgresql-otp

## Checklist complet pour refaire ce projet (React/Vite + Django + Koyeb/Render + Cloudflare)

Ce guide est réutilisable pour refaire un projet similaire (frontend + backend + CI/CD + déploiement).
Il est pensé pour être copié/collé et adapté à un nouveau projet.

---

### 1) Préparer le repo GitHub

- Créer un repo GitHub (public ou privé).
- Cloner localement le repo.
- Créer la structure :
  - `frontend/` (React Vite)
  - `backend/` (Django)
- Ajouter un `README.md` minimal.

---

### 2) Frontend (React + Vite)

- Créer le frontend :
  - `npm create vite@latest frontend -- --template react-ts`
- Installer les dépendances :
  - `cd frontend`
  - `npm install`
- Créer `.env.example` côté frontend :
  - `VITE_API_URL=https://<ton-backend>.koyeb.app/api`
- Utiliser `VITE_API_URL` dans le code (axios/baseURL).

---

### 3) Backend (Django + DRF)

- Créer le backend Django :
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `pip install django djangorestframework`
  - `django-admin startproject <project_name> backend`
- Ajouter les apps nécessaires (users, etc.).
- Configurer PostgreSQL dans `settings.py` via variables d’environnement :
  - `DB_HOST` / `DB_NAME` / `DB_USER` / `DB_PASS` / `DB_PORT`
- Créer `backend/.env.example` (sans secrets) :
  - `SECRET_KEY=...`
  - `DEBUG=False`
  - `DB_*`
  - `CORS_*`
  - `CSRF_TRUSTED_ORIGINS`
  - `EMAIL_*`

---

### 4) Dockeriser le backend

- Créer `backend/Dockerfile` (prod) :
  - Base `python:3.x-slim`
  - Installer `requirements.txt`
  - Copier le code
  - `CMD -> entrypoint.sh`
- Créer `backend/entrypoint.sh` :
  - migrate
  - collectstatic
  - `gunicorn --bind 0.0.0.0:$PORT`

---

### 5) GHCR (Docker Registry)

- Activer GitHub Container Registry (GHCR).
- Créer un workflow GitHub Actions :
  - build + push l’image Docker à chaque push sur `main`
  - tag : `ghcr.io/<user>/<repo>-backend:latest`

---

### 6) Base de données PostgreSQL (Koyeb ou Render)

- Koyeb **ou** Render → Databases → créer PostgreSQL
- Copier les Connection Details
- Récupérer :
  - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_PORT`
  - Sur Render, utilise le **Hostname** fourni (ex: `dpg-xxxx`).

---

### 7) Déployer le backend sur Koyeb

- Koyeb → Create Service → "Pre-built Docker image"
- Image : `ghcr.io/<user>/<repo>-backend:latest`
- Port : 8000 (HTTP)
- Variables d’env :
  - `DEBUG=False`
  - `SECRET_KEY=...`
  - `DB_*` (host, name, user, pass, port)
  - `CORS_ALLOW_ALL_ORIGINS=False`
  - `CORS_ALLOWED_ORIGINS=https://<ton-frontend>.pages.dev`
  - `CSRF_TRUSTED_ORIGINS=https://<ton-frontend>.pages.dev`
  - `EMAIL_*` (si email)
- Vérifier que Gunicorn écoute sur `0.0.0.0:$PORT`.

---

### 7bis) Déployer le backend sur Render (alternative simple)

- Render → New → **Web Service**
- Root Directory : `backend`
- Build Command :
  - `pip install -r requirements.txt`
  - `python manage.py collectstatic --noinput`
- Start Command :
  - `gunicorn agriculture.wsgi:application --bind 0.0.0.0:$PORT`
- Environment variables (Settings → Environment) :
  - `DEBUG=False`
  - `SECRET_KEY=...` (bouton **Generate** sur Render)
  - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_PORT`
  - `CORS_ALLOW_ALL_ORIGINS=False`
  - `CORS_ALLOWED_ORIGINS=https://<ton-frontend>.pages.dev`
  - `CSRF_TRUSTED_ORIGINS=https://<ton-frontend>.pages.dev`
- (Optionnel) Pre-deploy Command :
  - `python manage.py migrate`

---

### 8) Déployer le frontend sur Cloudflare Pages

- Cloudflare Pages → connecter le repo GitHub
- Root directory : `frontend`
- Build command : `npm ci && npm run build`
- Output : `dist`
- Environment variables (Production) :
  - `VITE_API_URL=https://<ton-backend>.koyeb.app/api`

---

### 9) CORS + CSRF

- Backend : `CORS_ALLOWED_ORIGINS` = domaine Cloudflare Pages
- Backend : `CSRF_TRUSTED_ORIGINS` = domaine Cloudflare Pages
- Ne pas laisser `CORS_ALLOW_ALL_ORIGINS=True` en prod.

---

### 10) CI/CD complet

- Push sur `main` → GitHub Actions build & push image (GHCR)
- Koyeb auto‑deploy → redéploiement automatique
- Cloudflare Pages → rebuild automatique du frontend

---

### 11) Vérifications finales

- Tester `/admin`, `/api/`, et login frontend
- Vérifier que les requêtes front → back passent (pas d’erreur CORS)
- Vérifier que la DB est bien utilisée (pas sqlite)
- Vérifier les logs Koyeb (migrations, gunicorn OK)
