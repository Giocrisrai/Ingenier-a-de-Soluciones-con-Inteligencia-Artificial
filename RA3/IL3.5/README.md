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
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-llm-applications/)
- [AWS Academy Learner Lab](https://www.awsacademy.com/)
- [Caddy — Automatic HTTPS](https://caddyserver.com/docs/automatic-https)
