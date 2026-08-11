# Presentación IL3.1 - Herramientas de Observabilidad y Métricas

## Slide 1: Título y Objetivos
**Título:** IL3.1 - Herramientas de Observabilidad y Métricas  
**Subtítulo:** Monitoreo y Medición de Agentes de IA

**Objetivos:**
- Implementar logging básico en agentes
- Medir métricas de rendimiento clave
- Registrar eventos importantes para debugging
- Establecer bases para monitoreo continuo

---

## Slide 2: ¿Por qué Observabilidad?
**Título:** Importancia del Monitoreo en Agentes IA

**Problemas sin observabilidad:**
- Agentes "caja negra" sin visibilidad interna
- Dificultad para detectar fallos o degradación
- Imposible optimizar sin datos de performance
- Debug reactivo en lugar de proactivo

**Beneficios del monitoreo:**
- **Detección temprana** de problemas
- **Optimización** basada en datos reales
- **Debugging** eficiente con logs estructurados
- **Confiabilidad** mejorada del sistema

---

## Slide 3: Observabilidad Básica - Implementación
**Título:** Script 1 - Logging y Métricas Simples

**Implementación práctica** (`1-observability_tools.py`, simulación sin llamar al modelo):
```python
class AgenteObservable:
    """Agente simulado que registra cada interaccion con metricas."""

    def procesar(self, mensaje: str) -> str:
        self.logger.info(f"Entrada: {mensaje!r}")
        inicio = time.perf_counter()
        ...
        duracion_ms = (time.perf_counter() - inicio) * 1000
        self.metricas.registrar(duracion_ms, tokens_in, tokens_out, exitoso=True)
        self.logger.info(f"Salida ({duracion_ms:.1f}ms, {tokens_in}+{tokens_out} tokens)")
        return respuesta
```

**Métricas capturadas por `RecolectorMetricas.resumen()`:**
- **`total_peticiones`:** Volumen de uso
- **`tiempo_promedio_ms` / `maximo` / `minimo`:** Performance del agente
- **`total_tokens`:** Consumo (base para estimar costo)
- **`tasa_errores_pct`:** Fiabilidad
- **Logs de entrada/salida con timestamp:** Trazabilidad completa

---

## Slide 4: Tipos de Métricas Clave
**Título:** Qué Medir en Agentes IA

**1. Métricas de Performance:**
- Tiempo de respuesta
- Throughput (mensajes/segundo)
- Latencia de herramientas externas
- Uso de recursos (CPU, memoria)

**2. Métricas de Calidad:**
- Tasa de éxito de tareas
- Precisión de respuestas
- Satisfacción del usuario
- Errores y excepciones

**3. Métricas de Negocio:**
- Volumen de interacciones
- Tipos de consultas
- Patrones de uso
- ROI de automatización

---

## Slide 5: Herramientas y Frameworks
**Título:** Stack de Observabilidad para Agentes

**Logging:**
- **Python logging:** Built-in, configuración simple
- **Structlog:** Logs estructurados en JSON
- **Loguru:** API moderna y simple

**Métricas:**
- **Prometheus:** Métricas de sistemas
- **Grafana:** Dashboards y visualización
- **Custom metrics:** Contadores y timers

**Distributed Tracing:**
- **OpenTelemetry:** Standard para tracing
- **Jaeger:** Distributed tracing system
- **LangSmith:** Específico para LLM/Agentes

**Alerting:**
- **Prometheus AlertManager:** Alertas automáticas
- **PagerDuty:** Gestión de incidentes
- **Custom webhooks:** Notificaciones específicas

---

## Slide 6: Mejores Prácticas
**Título:** Patrones de Observabilidad Efectiva

**Logging estructurado:**
```python
import structlog

logger = structlog.get_logger()
logger.info("agent_interaction", 
           agent_id="agent_001",
           user_input=message,
           response_time=duration,
           success=True)
```

**Métricas consistentes:**
- Usar nombres estándar para métricas
- Incluir labels relevantes (agent_id, user_type)
- Establecer umbrales de alerta
- Documentar significado de cada métrica

**Correlación de eventos:**
- Usar trace_id para seguir requests
- Correlacionar logs con métricas
- Mantener contexto entre llamadas

---

## Slide 7: Implementación en Producción
**Título:** De Prototipo a Sistema Monitoreado

**Configuración por ambiente:**
```python
# development
logging.basicConfig(level=logging.DEBUG)

# production  
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('/var/log/agent.log'),
        logging.StreamHandler()
    ]
)
```

**Dashboards esenciales:**
- Health status del agente
- Response time percentiles
- Error rate y tipos de errores
- Usage patterns y trends

**Alertas críticas:**
- Response time > umbral
- Error rate > 5%
- Agent down/unreachable
- Resource usage > 80%

---

## Slide 8: Próximos Pasos hacia IL3.2
**Título:** Evolución hacia Trazabilidad Completa

**Preparación para IL3.2:**
- Foundation sólida en métricas básicas
- Logs estructurados implementados
- Comprensión de observabilidad
- Base para análisis de trazas complejas

**IL3.2 - Análisis de Trazabilidad:**
- Tracing distribuido
- Análisis de logs avanzado
- Correlación de eventos
- Performance profiling

**Continuidad del proyecto:**
- Observabilidad como pilar de calidad
- Métricas para optimización continua
- Foundation para sistemas escalables
- Preparación para auditoría y compliance

---

## Slide 9: Resumen Ejecutivo
**Título:** Conceptos Clave del Módulo IL3.1

**Fundamentos establecidos:**
1. **Logging básico** con Python logging
2. **Métricas de performance** (tiempo, contador)
3. **Trazabilidad** de entrada y salida
4. **Foundation** para observabilidad avanzada

**Implementación práctica:**
- Agente con logging estructurado integrado (`1-observability_tools.py`)
- Medición de tiempo de respuesta, tokens y tasa de errores
- Reporte agregado en JSON con `RecolectorMetricas.resumen()`
- Notebook: dashboard con matplotlib y sistema de alertas por umbrales

**Valor organizacional:**
- Visibilidad en operaciones de agentes
- Base para optimización de performance
- Detección proactiva de problemas
- Foundation para escalabilidad

**Preparación para RA3 completo:**
- IL3.1: Observabilidad básica ✓
- IL3.2: Trazabilidad avanzada
- IL3.3: Seguridad y ética  
- IL3.4: Escalabilidad y sostenibilidad
- IL3.5: Ciberseguridad y despliegue en AWS