# Checklist de Seguridad y Despliegue (IL3.5)

## Antes de desplegar
- [ ] `.env` NO está en git (`git status` no lo muestra).
- [ ] El token de GitHub Models tiene solo los permisos necesarios.
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
- [ ] `/metrics` es público solo a propósito (demo de observabilidad); en
      producción se protege con token o IP interna.

## Después de la demo
- [ ] Recursos apagados/terminados para no gastar créditos.
- [ ] Capturas/evidencia guardadas para la entrega.
