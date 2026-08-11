# Backend FastAPI — imagen slim, usuario no-root.
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py agent.py guardrails.py ./

# Usuario sin privilegios
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8000/health'); sys.exit(0)" || exit 1

# IPs cuyo X-Forwarded-For se acepta. Por defecto solo localhost (valor seguro
# si alguien corre esta imagen suelta); docker-compose.prod.yml lo sobrescribe
# con la IP fija de Caddy.
ENV FORWARDED_ALLOW_IPS=127.0.0.1

# --proxy-headers + --forwarded-allow-ips: sin esto, uvicorn ignora
# X-Forwarded-For y `request.client.host` es SIEMPRE la IP del contenedor de
# Caddy. Resultado: el rate limiting de slowapi degenera en un único cubo
# global compartido por todos los usuarios (verificado: 25 IPs distintas
# agotaban la misma cuota de 20/minuto).
#
# Regla: aceptar X-Forwarded-For solo de un proxy de confianza que la
# reescriba. Nunca `*` en un servicio alcanzable desde Internet — ahí
# cualquiera falsifica su IP y el límite deja de existir.
#
# Forma `sh -c` para que se expanda la variable; `exec` mantiene a uvicorn como
# PID 1 y las señales de docker stop le llegan.
CMD ["sh", "-c", "exec uvicorn app:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips \"$FORWARDED_ALLOW_IPS\""]
