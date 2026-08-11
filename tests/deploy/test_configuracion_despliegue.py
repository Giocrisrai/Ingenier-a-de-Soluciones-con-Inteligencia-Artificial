"""Tests de configuración del despliegue.

El rate limiting por IP no depende solo del código Python: depende de tres
archivos que tienen que estar de acuerdo entre sí.

  Caddy reescribe X-Forwarded-For  ->  uvicorn confía en la IP de Caddy  ->
  slowapi ve la IP real del usuario

Si alguien cambia la subred en `docker-compose.prod.yml` y se olvida de
`FORWARDED_ALLOW_IPS`, o quita `--proxy-headers` del Dockerfile, no se rompe
ningún test de Python: simplemente el límite vuelve a ser un cubo global y nadie
se entera hasta que alguien lo abusa. Estos tests cierran ese hueco.
"""
import re
from pathlib import Path

DEPLOY = Path(__file__).resolve().parents[2] / "deploy"
DOCKERFILE_BACKEND = (DEPLOY / "backend" / "Dockerfile").read_text(encoding="utf-8")
COMPOSE = (DEPLOY / "docker-compose.prod.yml").read_text(encoding="utf-8")
CADDYFILE = (DEPLOY / "Caddyfile").read_text(encoding="utf-8")


def test_uvicorn_confia_en_las_cabeceras_del_proxy():
    # Sin esto, request.client.host es siempre la IP de Caddy y slowapi comparte
    # un único cubo de 20/minuto entre todos los usuarios.
    assert "--proxy-headers" in DOCKERFILE_BACKEND
    assert "--forwarded-allow-ips" in DOCKERFILE_BACKEND


def test_la_ip_de_confianza_es_la_de_caddy():
    ip_confiada = re.search(r'FORWARDED_ALLOW_IPS:\s*"([^"]+)"', COMPOSE).group(1)
    ip_caddy = re.search(r"ipv4_address:\s*([\d.]+)", COMPOSE).group(1)
    assert ip_confiada == ip_caddy, (
        "el backend confía en una IP que no es la de Caddy: el rate limiting "
        "por IP deja de funcionar en silencio"
    )
    # Y esa IP tiene que caer dentro de la subred declarada para la red interna.
    subred = re.search(r"subnet:\s*([\d.]+)/(\d+)", COMPOSE)
    assert ip_caddy.rsplit(".", 1)[0] == subred.group(1).rsplit(".", 1)[0]


def test_nunca_se_confia_en_cualquier_origen():
    # `*` significaría aceptar X-Forwarded-For de quien sea. En un servicio
    # alcanzable desde Internet eso equivale a no tener rate limiting.
    assert '"*"' not in re.search(r"FORWARDED_ALLOW_IPS:.*", COMPOSE).group(0)


def test_caddy_reescribe_x_forwarded_for():
    # La cabecera la escribe el proxy, nunca el cliente: si se dejara pasar el
    # valor del usuario, bastaría con inventar una IP distinta en cada petición.
    assert re.search(r"header_up\s+X-Forwarded-For\s+\{remote_host\}", CADDYFILE)


def test_solo_caddy_publica_puertos_al_host():
    # backend y frontend viven solo en la red interna.
    puertos = re.findall(r'ports:\s*\[([^\]]*)\]', COMPOSE)
    assert puertos == ['"80:80", "443:443"'], puertos
