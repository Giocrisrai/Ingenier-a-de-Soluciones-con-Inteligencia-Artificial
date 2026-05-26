# IL3.4: Escalabilidad y Sostenibilidad

Este módulo presenta estrategias y recomendaciones para diseñar agentes de IA que sean escalables, eficientes y sostenibles en entornos de producción.

## Objetivos de Aprendizaje

- Diseñar arquitecturas modulares para agentes escalables
- Monitorear y optimizar uso de recursos (tokens, memoria, API calls)
- Implementar estrategias de caching y rate limiting
- Automatizar despliegues y actualizaciones

## Archivos del Módulo

| Archivo | Descripción |
|---------|-------------|
| `1-scalability_sustainability.py` | Script principal con ejemplos de arquitectura modular, caching y monitoreo de recursos |
| `2-scalability-practice.ipynb` | Notebook práctico para implementar escalabilidad en un agente |
| `presentacion.md` | Diapositivas de apoyo con conceptos teóricos |

## Conceptos Clave

- **Modularidad**: División del sistema en componentes independientes
- **Caching**: Almacenamiento de respuestas frecuentes para reducir costos
- **Rate Limiting**: Control de frecuencia de llamadas a APIs
- **Monitoreo**: Seguimiento de uso de tokens, latencia y costo
- **Despliegue**: Automatización con CI/CD para actualizaciones frecuentes

## Cómo Empezar

```bash
# Ejecutar el script principal
uv run python RA3/IL3.4/1-scalability_sustainability.py

# Abrir el notebook práctico
uv run jupyter lab RA3/IL3.4/2-scalability-practice.ipynb
```

## Recursos

- [System Design for AI](https://github.com/microsoft/ai-system)
- [LangServe Deployment](https://python.langchain.com/docs/langserve)
- [Docker Compose for ML](https://docs.docker.com/compose/)