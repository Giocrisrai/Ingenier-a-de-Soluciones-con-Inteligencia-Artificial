# IL3.5 — Ciberseguridad y Despliegue en AWS

## 1. ¿Por qué este módulo?
RA3 ya cubre observabilidad y seguridad del agente. Falta: llevar la solución a
producción de forma **segura** y **reproducible**.

## 2. Arquitectura
Internet → Caddy (HTTPS) → Streamlit → FastAPI (agente + guardrails) → GitHub Models.
Solo el proxy se expone; el resto vive en una red interna de Docker.

## 3. Esenciales de ciberseguridad
- Secretos fuera del repo (.env / SSM).
- Mínimo privilegio: Security Group + LabRole.
- HTTPS + cabeceras de seguridad.
- Rate limiting y validación de entrada.

## 4. OWASP LLM Top 10 (aplicado)
- LLM01 Prompt Injection → validación de entrada (mensaje e historial).
- LLM02 Insecure Output → escapado de la salida.
- LLM04 DoS → rate limiting + límite de longitud y presupuesto acumulado.
- LLM06 Info Disclosure → no exponer trazas; redacción de PII.

## 5. Despliegue en AWS Academy
1 EC2 + Docker Compose. Pasos en `1-deploy-aws-paso-a-paso.md`.

## 6. Cierre
Verificar → demostrar → **apagar recursos**.
