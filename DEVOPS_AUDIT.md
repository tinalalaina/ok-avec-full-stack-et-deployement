# Audit DevOps rapide du projet

## État global

Le projet **n'est pas encore totalement finalisé côté DevOps**.

## Ce qui est déjà en place

- Dockerisation du backend (`backend/Dockerfile`, `backend/entrypoint.sh`).
- Workflow GitHub Actions pour build/push de l'image backend vers GHCR (`.github/workflows/backend-ghcr.yml`).
- Configuration backend orientée variables d'environnement (DB, CORS/CSRF, email) dans `backend/agriculture/settings.py`.
- Documentation de base pour le déploiement frontend (`frontend/README.md`) et checklist globale (`README.md`).

## Reste à faire (priorité haute)

1. **Retirer les secrets du repo et faire une rotation immédiate**
   - Le fichier `backend/env` versionné contient des identifiants email réels.
   - Actions recommandées:
     - révoquer/changer les mots de passe exposés,
     - supprimer les secrets de l'historique Git,
     - versionner uniquement un `backend/.env.example` sans secrets.

2. **Sécuriser la configuration Django de production**
   - Remplacer `ALLOWED_HOSTS = ["*"]` par une liste stricte via variable d'environnement.
   - Renforcer les paramètres de sécurité HTTP (SECURE_* et cookies) selon l'hébergement.

3. **Compléter la CI/CD qualité (pas seulement build image)**
   - Ajouter des jobs CI pour:
     - lint backend + frontend,
     - tests backend + frontend,
     - build frontend.
   - Ajouter le déclenchement sur PR (pas uniquement sur push `main`).

4. **Formaliser la stratégie d'environnements**
   - Standardiser les fichiers `.env.example` (frontend et backend).
   - Documenter clairement les variables obligatoires par environnement (local/staging/prod).

5. **Mettre en place l'observabilité minimale**
   - Centralisation des logs backend,
   - alertes basiques (erreurs 5xx, échecs de déploiement),
   - endpoint de healthcheck documenté pour la plateforme de déploiement.

## Reste à faire (priorité moyenne)

6. **Durcir la chaîne Docker**
   - Ajouter un scan de vulnérabilités image (ex: Trivy) dans la CI.
   - Envisager un utilisateur non-root dans l'image.

7. **Process de migration DB plus robuste**
   - Conserver la migration auto si souhaité, mais définir une stratégie explicite (pre-deploy command, rollback, backup).

8. **Documentation runbook**
   - Écrire une procédure d'incident (panne DB, rollback backend, restauration).

## Conclusion

Le socle DevOps existe (Docker + GHCR + base de déploiement), mais il manque encore des éléments critiques de sécurité, de CI qualité et d'exploitation pour considérer le DevOps comme "terminé".
