# IL3.1: Herramientas de Observabilidad y Métricas

En este módulo aprenderás a agregar logs, métricas y monitoreo a tus agentes de IA para comprender su funcionamiento, diagnosticar problemas y medir desempeño en producción.

## Objetivos de Aprendizaje

- Implementar logging estructurado en agentes de IA
- Medir tiempos de respuesta y latencia de llamadas a modelos
- Registrar eventos clave (errores, decisiones, llamadas a herramientas)
- Visualizar métricas básicas de rendimiento

## Archivos del Módulo

| Archivo | Descripción |
|---------|-------------|
| `1-observability_tools.py` | Script principal con ejemplos de logging, medición de tiempo y registro de eventos en un agente |
| `2-observability-practice.ipynb` | Notebook práctico para implementar observabilidad en un agente conversacional |
| `presentacion.md` | Diapositivas de apoyo con conceptos teóricos |

## Conceptos Clave

- **Logging**: Registro cronológico de eventos, errores y decisiones del agente
- **Métricas**: KPIs como tiempo de respuesta, tasa de éxito, tokens utilizados
- **Trazabilidad**: Capacidad de reconstruir el flujo de decisiones del agente
- **Monitoreo**: Observación continua del sistema para detectar anomalías

## Cómo Empezar

```bash
# Ejecutar el script principal
uv run python RA3/IL3.1/1-observability_tools.py

# Abrir el notebook práctico
uv run jupyter lab RA3/IL3.1/2-observability-practice.ipynb
```

## Recursos

- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [LangSmith Tracing](https://docs.smith.langchain.com/tracing)
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
