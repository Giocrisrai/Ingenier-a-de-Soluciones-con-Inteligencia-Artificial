# IL3.3: Seguridad y Ética en Agentes de IA

Este módulo cubre las mejores prácticas para proteger tus agentes de IA contra usos malintencionados y garantizar un comportamiento ético y responsable.

## Objetivos de Aprendizaje

- Validar entradas de usuario para prevenir injection de prompts
- Implementar guardrails y restricciones de seguridad
- Diseñar respuestas responsables y libres de sesgos
- Evaluar implicaciones éticas del despliegue de agentes

## Archivos del Módulo

| Archivo | Descripción |
|---------|-------------|
| `1-security_ethics.py` | Script principal con ejemplos de validación de entradas, sanitización y respuestas responsables |
| `2-security-ethics-practice.ipynb` | Notebook práctico para implementar seguridad y ética en un agente |
| `presentacion.md` | Diapositivas de apoyo con conceptos teóricos |

## Conceptos Clave

- **Prompt Injection**: Prevención de instrucciones maliciosas en entradas de usuario
- **Guardrails**: Barreras de protección para limitar acciones del agente
- **Sesgos**: Identificación y mitigación de sesgos en respuestas
- **Privacidad**: Protección de datos sensibles en interacciones
- **Transparencia**: Comunicación clara de limitaciones y capacidades

## Cómo Empezar

```bash
# Ejecutar el script principal
uv run python RA3/IL3.3/1-security_ethics.py

# Abrir el notebook práctico
uv run jupyter lab RA3/IL3.3/2-security-ethics-practice.ipynb
```

## Recursos

- [OWASP LLM Security](https://owasp.org/www-project-top-10-for-llm-applications/)
- [Responsible AI Practices](https://www.microsoft.com/en-us/ai/responsible-ai)
- [Anthropic Responsible Scaling Policy](https://www.anthropic.com/news/announcing-our-responsible-scaling-policy)
