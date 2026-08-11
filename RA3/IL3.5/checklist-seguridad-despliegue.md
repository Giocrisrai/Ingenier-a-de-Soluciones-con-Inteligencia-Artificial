# Checklist de Seguridad y Despliegue (IL3.5)

## Antes de desplegar
- [ ] `.env` NO está en git (`git status` no lo muestra).
- [ ] La `GROQ_API_KEY` está solo en el `.env` del servidor (nunca en git) y se
      puede revocar desde https://console.groq.com/keys.
- [ ] Los contenedores corren como usuario no-root.
- [ ] Solo el proxy publica puertos; backend/frontend en red interna.

## En AWS
- [ ] Security Group: 443/80 abiertos; 22 solo a mi IP (no 0.0.0.0/0).
- [ ] La instancia usa el rol `LabRole` (no claves embebidas).
- [ ] HTTPS funciona y redirige desde HTTP.

## Seguridad de la app (OWASP LLM)
- [ ] Prompt injection bloqueado en el mensaje y en el historial (probado).
- [ ] Rate limiting devuelve 429 al exceder el límite.
- [ ] La salida del modelo se muestra escapada (sin HTML crudo).
- [ ] PII redactada en respuestas y logs.
- [ ] Los errores no exponen trazas internas al cliente.
- [ ] Sé explicar **qué NO cubre** mi guardrail: es un filtro por patrones, evadible con otro
      idioma o codificación, y **no ve la inyección indirecta** (la que llega dentro de un
      documento, una web o la salida de una herramienta).
- [ ] Si mi agente tiene herramientas: cada una con el **mínimo permiso** necesario, y las
      acciones irreversibles (borrar, pagar, enviar) piden **confirmación humana**.
- [ ] `/metrics` es público solo a propósito (demo de observabilidad); en
      producción se protege con token o IP interna.

## Después de la demo
- [ ] Recursos apagados/terminados para no gastar créditos.
- [ ] Capturas/evidencia guardadas para la entrega.
