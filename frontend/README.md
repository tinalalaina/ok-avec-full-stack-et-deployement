# Frontend (React + Vite)

## Configuration essentielle

Crée un fichier `frontend/.env` (ou configure la variable sur Cloudflare Pages) avec :

```env
VITE_API_URL=https://ok-avec-full-stack-et-deployement.onrender.com/api
```

> Important : l'URL doit pointer vers `/api` (pas seulement la racine du backend).

## Variables d'environnement recommandées

- Local (`frontend/.env`) :

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

- Production (`frontend/.env.production`) :

```env
VITE_API_URL=https://ok-avec-full-stack-et-deployement.onrender.com/api
```


## CI (GitHub Actions)

Le workflow `frontend-ci.yml` valide le lint puis le build frontend sur chaque `pull_request` et sur `main` (uniquement si des fichiers frontend changent).

## Développement local

```bash
cd frontend
npm install
npm run dev
```

## Build production

```bash
cd frontend
npm run build
```

## Déploiement Cloudflare Pages

- Root directory : `frontend`
- Build command : `npm ci && npm run build`
- Output directory : `dist`
- Variable d'environnement :
  - `VITE_API_URL=https://ok-avec-full-stack-et-deployement.onrender.com/api`
