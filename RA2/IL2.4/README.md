# IL2.4: Documentacion Tecnica y Diseno de Arquitectura

## Descripcion

Modulo dedicado a las mejores practicas para documentar sistemas de agentes LLM y disenar arquitecturas escalables. Se cubren patrones de diseno, documentacion tecnica y estrategias de implementacion para proyectos basados en agentes inteligentes.

## Objetivos de Aprendizaje

- Comprender patrones de arquitectura para sistemas de agentes
- Crear documentacion tecnica efectiva para proyectos de IA
- Disenar arquitecturas escalables y mantenibles
- Aplicar buenas practicas de desarrollo en proyectos de agentes

## Archivos del Modulo

| Archivo | Descripcion |
|---------|-------------|
| [1-architecture_example.py](1-architecture_example.py) | Ejemplo practico de arquitectura en capas: `AgenteOrquestador` enruta a herramientas registradas (`calculadora`, `buscador`, `traductor`), con separacion dominio / infraestructura / aplicacion / presentacion. |
| [2-best_practices.py](2-best_practices.py) | Buenas practicas **implementadas**, no listadas: configuracion centralizada desde variables de entorno (`Configuracion.desde_entorno`), validacion de la entrada del usuario, reintentos con backoff exponencial y manejo de errores estructurado (`ResultadoOperacion`). |
| [presentacion.md](presentacion.md) | Material de presentacion con 10 slides que cubren documentacion tecnica, patrones de arquitectura, testing, deployment y gestion del ciclo de vida. |

## Antes de empezar

Los dos scripts son **autocontenidos**: no llaman a ningun LLM, no necesitan `GROQ_API_KEY` ni
conexion a internet. Se ejecutan directamente con `python 1-architecture_example.py` y
`python 2-best_practices.py`.

`2-best_practices.py` simula la llamada a la API (con fallos aleatorios) a proposito, para que
el patron de reintento se pueda observar sin gastar cuota. Por eso usa nombres de variable
genericos (`API_KEY`, `MODELO_LLM`); en el resto del curso el equivalente real es
`GROQ_API_KEY` y `GROQ_MODEL`.

## Material de Presentacion

Para ver las diapositivas completas del modulo, consultar [presentacion.md](presentacion.md).
