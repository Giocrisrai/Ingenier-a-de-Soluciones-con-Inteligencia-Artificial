# IL3.5: Ciberseguridad y Despliegue en AWS

Este módulo lleva la app del curso a un despliegue real y seguro en AWS Academy,
cerrando RA3: de la observabilidad (IL3.1/3.2) y la seguridad del agente (IL3.3)
a la **ciberseguridad de la aplicación/infraestructura** y el **despliegue correcto**.

## Objetivos de Aprendizaje
- Empaquetar una solución de IA (frontend + API) en contenedores.
- Aplicar esenciales de ciberseguridad: secretos, mínimo privilegio, HTTPS,
  rate limiting y mitigación del OWASP LLM Top 10.
- Desplegar en una EC2 de AWS Academy Learner Lab paso a paso.
- Verificar y luego apagar recursos para cuidar los créditos.

## Archivos del Módulo
| Archivo | Descripción |
|---|---|
| `1-deploy-aws-paso-a-paso.md` | Guía completa de despliegue en AWS Academy. |
| `2-security-hardening-practice.ipynb` | Práctica: guardrails y ataque/mitigación de prompt injection. |
| `checklist-seguridad-despliegue.md` | Checklist para la entrega/presentación. |
| `presentacion.md` | Diapositivas de apoyo. |

## Artefacto desplegable
El código vive en la carpeta raíz [`deploy/`](../../deploy/README.md).

## Conceptos Clave
- **Contenedores no-root** y red interna (solo el proxy se expone).
- **HTTPS** con Caddy + cabeceras de seguridad (HSTS, X-Content-Type-Options).
- **Mínimo privilegio**: Security Group restrictivo, rol `LabRole`.
- **Secretos** fuera del repo (`.env` / SSM Parameter Store).
- **OWASP LLM Top 10** aplicado en el backend.

## Recursos
- [OWASP GenAI LLM Top 10 — edición 2026 (lista vigente, publicada en agosto de 2026)](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
  — la presentación usa estos códigos y muestra la equivalencia con los de 2025 y 2023, porque
  la numeración **cambia en cada edición**.
- [OWASP Top 10 for Agentic Applications 2026 (ASI01–ASI10)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
  — lista específica para agentes: secuestro de objetivo, abuso de herramientas, envenenamiento
  de memoria/contexto, comunicación insegura entre agentes.
- [AWS Academy Learner Lab](https://www.awsacademy.com/)
- [Caddy — Automatic HTTPS](https://caddyserver.com/docs/automatic-https)
