# IL3.5 — Ciberseguridad y Despliegue en AWS

## 1. ¿Por qué este módulo?
RA3 ya cubre observabilidad y seguridad del agente. Falta: llevar la solución a
producción de forma **segura** y **reproducible**.

## 2. Arquitectura
Internet → Caddy (HTTPS) → Streamlit → FastAPI (agente + guardrails) → Groq (LPU).
Solo el proxy se expone; el resto vive en una red interna de Docker.

## 3. Esenciales de ciberseguridad
- Secretos fuera del repo (.env / SSM).
- Mínimo privilegio: Security Group + LabRole.
- HTTPS + cabeceras de seguridad.
- Rate limiting y validación de entrada.

## 4. OWASP LLM Top 10 (aplicado)
La lista **vigente es la 2026** (publicada a comienzos de agosto de 2026,
https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/). Abajo, el código 2026 y,
entre paréntesis, los códigos antiguos que aún circulan en apuntes y blogs.

- **LLM01:2026 Prompt Injection** (= LLM01:2025 = LLM01 de 2023) → validación de entrada
  (mensaje e historial).
- **LLM10:2026 Improper Output Handling** (LLM05:2025; "Insecure Output" en 2023) → escapado
  de la salida.
- **LLM06:2026 Unbounded Consumption** (LLM10:2025; "DoS" en 2023) → rate limiting + límite de
  longitud y presupuesto acumulado.
- **LLM02:2026 Sensitive Information Disclosure** (= LLM02:2025; LLM06 en 2023) → no exponer
  trazas; redacción de PII.

> Los números **cambian entre ediciones**: citar "LLM04 = DoS" sin decir de qué año es hoy un
> error. Escribe siempre el año en el código (`LLM06:2026`).

### Lo que este artefacto **no** mitiga (y hay que decirlo en la defensa)
El backend es un ejemplo didáctico. Riesgos vigentes que quedan fuera de su alcance:

- **Prompt injection indirecta**: la instrucción maliciosa no la escribe el usuario, viene
  dentro de un documento, una página web o el resultado de una herramienta. Nuestro guardrail
  solo inspecciona lo que teclea el usuario, así que **no la vería**. Es el vector más
  peligroso porque salta el punto donde estamos mirando.
- **LLM03:2026 Excessive Agency**: nuestro agente no tiene herramientas. En cuanto un agente
  pueda borrar, pagar o enviar correos, el control ya no es el filtro de entrada sino el
  **mínimo privilegio de la herramienta** y la **aprobación humana** para acciones
  irreversibles.
- **LLM09:2026 Vector and Embedding Weaknesses** / envenenamiento del contexto en RAG: si el
  agente recupera documentos, quien logre insertar un documento controla parte del prompt.
- **LLM08:2026 Hidden Context Exposure** (antes *System Prompt Leakage*): el system prompt no
  es un secreto; asume que se puede extraer y no pongas credenciales ni reglas de negocio
  sensibles en él.

## 5. Despliegue en AWS Academy
1 EC2 + Docker Compose. Pasos en `1-deploy-aws-paso-a-paso.md`.

## 6. Cierre
Verificar → demostrar → **apagar recursos**.
