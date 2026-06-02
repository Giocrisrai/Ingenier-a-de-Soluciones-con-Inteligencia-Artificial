# deploy/ — Artefacto desplegable

App del curso lista para producción mínima: frontend Streamlit + API FastAPI con
guardrails + proxy Caddy (HTTPS). Pensado para AWS Academy Learner Lab (1 EC2 + Docker Compose).

## Correr en local

```bash
cp deploy/.env.example deploy/.env   # completa GITHUB_TOKEN si quieres respuestas reales
docker compose -f deploy/docker-compose.prod.yml up --build
```

- Frontend: https://localhost (Caddy, certificado self-signed → acepta el aviso)
- Backend health: `curl -k https://localhost/api/health`

Sin `GITHUB_TOKEN` el backend responde en **modo demo** (sin llamar al modelo), útil para probar la infraestructura.

## Despliegue en AWS

Ver `RA3/IL3.5/1-deploy-aws-paso-a-paso.md`.
