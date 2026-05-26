# IL3.2: Análisis de Trazabilidad y Logs

Este módulo profundiza en cómo analizar y aprovechar los logs generados por los agentes para entender su comportamiento, depurar errores y realizar auditorías.

## Objetivos de Aprendizaje

- Implementar sistemas de trazabilidad en agentes de IA
- Analizar logs para identificar patrones de error
- Correlacionar eventos a través del flujo del agente
- Utilizar logs para auditoría y cumplimiento

## Archivos del Módulo

| Archivo | Descripción |
|---------|-------------|
| `1-traceability_analysis.py` | Script principal con ejemplos de guardado, lectura y análisis de logs de agentes |
| `2-traceability-practice.ipynb` | Notebook práctico para implementar trazabilidad y depuración |
| `presentacion.md` | Diapositivas de apoyo con conceptos teóricos |

## Conceptos Clave

- **Trazabilidad**: Seguimiento del flujo completo de decisión del agente
- **Correlación**: Relacionar eventos, prompts y respuestas en una sola traza
- **Depuración**: Uso de logs para identificar causas de fallos
- **Auditoría**: Registro permanente de interacciones para revisión posterior

## Cómo Empezar

```bash
# Ejecutar el script principal
uv run python RA3/IL3.2/1-traceability_analysis.py

# Abrir el notebook práctico
uv run jupyter lab RA3/IL3.2/2-traceability-practice.ipynb
```

## Recursos

- [Python Traceback Module](https://docs.python.org/3/library/traceback.html)
- [Structured Logging](https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging)
- [OpenTelemetry Traces](https://opentelemetry.io/docs/concepts/signals/traces/)
