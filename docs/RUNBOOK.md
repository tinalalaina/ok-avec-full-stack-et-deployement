# Runbook exploitation

## Vérification de santé
- Endpoint: `GET /healthz/`
- Résultat attendu: `200` et `{"status":"ok"}`.

## Déploiement backend
1. Build/push image via GitHub Actions (`backend-ghcr.yml`).
2. Déployer la nouvelle image sur la plateforme.
3. Vérifier les logs de démarrage (`migrate`, `collectstatic`, `gunicorn`).
4. Vérifier `/healthz/`.

## Incident: backend indisponible
1. Vérifier les logs applicatifs de la plateforme.
2. Vérifier la connectivité DB (`DB_*` / `DATABASE_URL`).
3. Vérifier variables CORS/CSRF/ALLOWED_HOSTS.
4. Rollback vers l'image précédente si nécessaire.

## Incident: migration échoue
1. Analyser la migration fautive et corriger.
2. Redéployer avec migration corrigée.
3. Si critique, rollback applicatif + restauration DB depuis backup provider.

## Incident: secrets exposés
1. Révoquer immédiatement les secrets compromis.
2. Générer et injecter de nouveaux secrets dans l'environnement.
3. Purger l'historique Git si nécessaire.
4. Vérifier l'absence de secrets dans le repo avant nouveau déploiement.
