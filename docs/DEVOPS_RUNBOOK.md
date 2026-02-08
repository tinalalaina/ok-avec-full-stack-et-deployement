# DevOps Runbook (Production)

## 1) Pre-deploy checklist

- Backend CI green (`backend-ghcr.yml` quality + build).
- Frontend CI green (`frontend-ci.yml`).
- Security checks green (`security.yml`).
- Required secrets configured on platforms (Koyeb/Render/Cloudflare).

## 2) Deployment procedure

1. Merge into `main`.
2. Verify backend image push to GHCR.
3. Verify backend platform auto-deploy completed.
4. Verify frontend Cloudflare Pages deployment completed.
5. Run smoke checks:

```bash
BACKEND_URL=https://<backend-domain> FRONTEND_URL=https://<frontend-domain> ./scripts/devops_smoke_check.sh
```

## 3) Post-deploy validation

- `GET /healthz/` returns HTTP 200 with `{"status":"ok","db":"ok"}`.
- Frontend login works.
- Protected API endpoint (`/api/users/user-info/`) accessible with JWT.
- CORS works from frontend production domain.

## 4) Rollback

### Backend rollback

- Redeploy previous known-good GHCR image tag (`ghcr.io/<org>/<repo>-backend:<sha>`).
- Re-run smoke checks.

### Frontend rollback

- Promote previous successful Cloudflare Pages deployment.
- Re-run smoke checks.

## 5) Incident quick actions

- API down: check platform logs first, then DB connectivity.
- 5xx spikes: inspect latest deployment diff and rollback if needed.
- Auth failures: verify JWT config + system time + CORS/CSRF origins.

## 6) Ownership

- Backend owner: team backend
- Frontend owner: team frontend
- DevOps owner: team platform
