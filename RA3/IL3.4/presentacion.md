# Presentación IL3.4 - Escalabilidad y Sostenibilidad

## Slide 1: Título y Objetivos
**Título:** IL3.4 - Escalabilidad y Sostenibilidad  
**Subtítulo:** Optimización y Mantenimiento a Largo Plazo de Sistemas IA

**Objetivos:**
- Diseñar sistemas escalables horizontalmente
- Implementar prácticas de sostenibilidad en IA
- Optimizar consumo de recursos y costos
- Establecer estrategias de mantenimiento a largo plazo

---

## Slide 2: ¿Por qué Escalabilidad y Sostenibilidad?
**Título:** Desafíos del Crecimiento de Sistemas IA

**Problemas de escalabilidad:**
- **Performance degradation:** Sistema lento con más usuarios
- **Resource exhaustion:** CPU/memoria/storage insuficientes
- **Cost explosion:** Gastos descontrolados con el crecimiento
- **Maintenance overhead:** Complejidad creciente difícil de mantener

**Beneficios de sistemas escalables:**
- **Growth ready:** Manejo de demanda creciente
- **Cost efficiency:** Optimización de recursos y gastos
- **Reliability:** Sistemas robustos ante picos de carga
- **Future-proof:** Adaptabilidad a cambios tecnológicos

**Sostenibilidad como imperativo:**
- Responsabilidad ambiental con el consumo energético
- Eficiencia económica a largo plazo
- Mantenibilidad del código y arquitectura

---

## Slide 3: Principios de Escalabilidad
**Título:** Script 1 - Fundamentos para Sistemas Escalables

**Lo que implementa** (`1-scalability_sustainability.py`, simulación sin llamar al modelo):
```python
cache = CacheLLM(tamano_maximo=50)   # hash SHA-256 del par (modelo, prompt)

def seleccionar_modelo(prompt: str) -> ConfigModelo:
    """Enruta segun complejidad: rapido / estandar / avanzado."""
    return MODELOS_DISPONIBLES[clasificar_complejidad(prompt)]

# Cada peticion: cache -> enrutamiento -> costo estimado por tokens
resultados = procesar_lote(prompts, cache)
```

**Principios clave del script:**
- **Caché:** evitar pagar dos veces por la misma respuesta
- **Enrutamiento de modelos:** el modelo barato para lo simple (`llama-3.1-8b-instant`)
- **Procesamiento por lotes:** agrupar peticiones en vez de una a una
- **Medición de costo:** estimar USD por petición a partir de los tokens
- **Resource monitoring:** monitorear y ajustar según demanda

**Arquitectura escalable básica:**
```
Load Balancer → [Agent 1, Agent 2, Agent N] → Message Queue → Workers
```

---

## Slide 4: Escalabilidad Horizontal vs Vertical
**Título:** Estrategias de Crecimiento de Sistemas

**Escalabilidad Vertical (Scale Up):**
- Más CPU, RAM, almacenamiento en misma máquina
- **Ventaja:** Simple de implementar
- **Desventaja:** Límite físico, single point of failure

**Escalabilidad Horizontal (Scale Out):**
```python
class HorizontalAgent:
    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.load_balancer = LoadBalancer()
    
    def distribute_request(self, request):
        available_instances = self.get_healthy_instances()
        chosen_instance = self.load_balancer.select(available_instances)
        return chosen_instance.process(request)
```

**Ventajas horizontales:**
- Sin límite teórico de crecimiento
- Fault tolerance distribuida
- Cost-effective para grandes volúmenes

**Implementación con containers:**
```dockerfile
# Agente containerizado (el artefacto real de IL3.5 usa esta misma base)
FROM python:3.11-slim-bookworm
COPY agent.py /app/
WORKDIR /app
CMD ["python", "agent.py"]
```

---

## Slide 5: Optimización de Recursos
**Título:** Eficiencia en Consumo de CPU, Memoria y Red

**CPU Optimization:**
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class OptimizedAgent:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def process_batch(self, requests):
        # Procesamiento paralelo de requests
        tasks = [
            asyncio.get_event_loop().run_in_executor(
                self.executor, self.process_single, req
            ) for req in requests
        ]
        return await asyncio.gather(*tasks)
```

**Memory Management:**
```python
class MemoryEfficientAgent:
    def __init__(self):
        self.cache = {}
        self.max_cache_size = 1000
    
    def process_with_cache(self, input_data):
        cache_key = hash(str(input_data))
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = self.expensive_computation(input_data)
        
        # LRU cache management
        if len(self.cache) >= self.max_cache_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[cache_key] = result
        return result
```

**Network Optimization:**
- Connection pooling para APIs externas
- Compression de requests/responses
- Batch requests cuando sea posible
- CDN para assets estáticos

---

## Slide 6: Arquitecturas para Escalabilidad
**Título:** Patrones de Diseño Escalables

**1. Microservicios de Agentes:**
```python
# Agent Service
class AgentService:
    def __init__(self, service_name):
        self.service_name = service_name
        self.health_endpoint = "/health"
    
    def register_with_discovery(self):
        # Service discovery registration
        pass

# API Gateway
class APIGateway:
    def route_request(self, request):
        service = self.service_discovery.find_service(request.type)
        return service.process(request)
```

**2. Event-Driven Architecture:**
```python
class EventDrivenAgent:
    def __init__(self):
        self.event_bus = EventBus()
        self.subscribe_to_events()
    
    def handle_user_request(self, event):
        # Process asynchronously
        self.event_bus.publish("processing_started", event.data)
        result = self.process(event.data)
        self.event_bus.publish("processing_completed", result)
```

**3. CQRS (Command Query Responsibility Segregation):**
- Separar operaciones de lectura y escritura
- Optimizar cada path independientemente
- Scaling diferenciado según uso

---

## Slide 7: Sostenibilidad y Green Computing
**Título:** IA Responsable con el Medio Ambiente

**Green AI Principles:**
- **Efficiency first:** Optimizar antes de escalar
- **Carbon awareness:** Considerar huella de carbono
- **Resource minimization:** Usar solo recursos necesarios
- **Renewable energy:** Preferir data centers verdes

**Implementación práctica:**
```python
class SustainableAgent:
    def __init__(self):
        self.carbon_tracker = CarbonTracker()
        self.energy_optimizer = EnergyOptimizer()
    
    def process_with_carbon_awareness(self, request):
        # Verificar intensidad de carbono actual
        carbon_intensity = self.carbon_tracker.get_current_intensity()
        
        if carbon_intensity > self.threshold:
            # Diferir procesamiento no crítico
            return self.schedule_for_low_carbon_time(request)
        
        return self.process_immediately(request)
    
    def optimize_model_size(self):
        # Model pruning, quantization
        return self.energy_optimizer.compress_model(self.model)
```

**Métricas de sostenibilidad:**
- Energy consumption per request
- Carbon footprint por operación
- Resource utilization efficiency
- Model accuracy vs energy trade-offs

---

## Slide 8: Automatización y DevOps
**Título:** Operations Eficientes para Sistemas Escalables

**CI/CD Pipeline:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Scalable Agent
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7
      
      - name: Build Docker Image
        run: docker build -t agent:${{ github.sha }} .
      
      - name: Run Tests
        run: docker run agent:${{ github.sha }} pytest
      
      - name: Deploy to Kubernetes
        run: kubectl set image deployment/agent agent=agent:${{ github.sha }}
```

**Infrastructure as Code:**
```python
# terraform/main.tf for agent infrastructure
resource "aws_ecs_cluster" "agent_cluster" {
  name = "scalable-agents"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "agent_service" {
  name            = "agent-service"
  cluster         = aws_ecs_cluster.agent_cluster.id
  task_definition = aws_ecs_task_definition.agent.arn
  desired_count   = 3
  
  deployment_configuration {
    minimum_healthy_percent = 50
    maximum_percent         = 200
  }
}
```

**Auto-scaling:**
```python
class AutoScaler:
    def __init__(self):
        self.metrics = MetricsCollector()
        self.orchestrator = ContainerOrchestrator()
    
    def check_scaling_needed(self):
        cpu_usage = self.metrics.get_avg_cpu_usage()
        memory_usage = self.metrics.get_avg_memory_usage()
        request_rate = self.metrics.get_request_rate()
        
        if cpu_usage > 70 or memory_usage > 80:
            self.scale_up()
        elif cpu_usage < 30 and memory_usage < 40:
            self.scale_down()
```

---

## Slide 9: Monitoring y Alerting para Escalabilidad
**Título:** Observabilidad de Sistemas Distribuidos

**Métricas clave de escalabilidad:**
```python
class ScalabilityMetrics:
    def collect_metrics(self):
        return {
            # Performance metrics
            "response_time_p95": self.get_percentile_response_time(95),
            "throughput_rps": self.get_requests_per_second(),
            "error_rate": self.get_error_rate(),
            
            # Resource metrics
            "cpu_utilization": self.get_cpu_usage(),
            "memory_utilization": self.get_memory_usage(),
            "disk_io": self.get_disk_io(),
            
            # Business metrics
            "cost_per_request": self.calculate_cost_per_request(),
            "user_satisfaction": self.get_user_satisfaction_score(),
            
            # Sustainability metrics
            "energy_per_request": self.get_energy_consumption(),
            "carbon_footprint": self.calculate_carbon_footprint()
        }
```

**Alerting rules:**
- Response time > 2 seconds
- Error rate > 5%
- CPU utilization > 80%
- Cost increase > 20% week-over-week
- Carbon footprint above sustainability target

---

## Slide 10: Proyecto Final RA3 y Resumen
**Título:** Integración Completa de Observabilidad, Seguridad y Escalabilidad

**Arquitectura final del proyecto RA3:**
```
┌─────────────────────────────────────────────────┐
│           Scalable & Sustainable System         │
├─────────────────────────────────────────────────┤
│ IL3.5: Ciberseguridad y Despliegue en AWS      │
├─────────────────────────────────────────────────┤
│ IL3.4: Escalabilidad y Sostenibilidad          │
├─────────────────────────────────────────────────┤
│ IL3.3: Seguridad y Ética                       │
├─────────────────────────────────────────────────┤
│ IL3.2: Trazabilidad y Análisis                 │
├─────────────────────────────────────────────────┤
│ IL3.1: Observabilidad y Métricas               │
└─────────────────────────────────────────────────┘
```

**Conceptos clave aprendidos:**
1. **Escalabilidad horizontal** con microservicios y containers
2. **Sostenibilidad** con green computing y optimización
3. **Automatización** con CI/CD y infrastructure as code
4. **Monitoring avanzado** para sistemas distribuidos

**Valor organizacional del proyecto completo:**
- **Sistemas production-ready** con observabilidad completa
- **Security by design** con ethical frameworks
- **Scalable architecture** preparada para crecimiento
- **Sustainable operations** con responsabilidad ambiental

**Foundation para el futuro:**
- Base sólida para sistemas empresariales
- Preparación para regulaciones emergentes
- Framework para innovación responsable
- Platform para transformación digital sostenible