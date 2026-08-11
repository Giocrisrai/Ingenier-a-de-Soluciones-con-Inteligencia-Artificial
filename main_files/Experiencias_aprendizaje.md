# EXPERIENCIAS DE APRENDIZAJE

## EA 1 - Fundamentos de IA Generativa y Prompt Engineering

**Resultado de Aprendizaje:** RA1

**Descripción:**
En la primera experiencia de aprendizaje, las/los estudiantes desarrollan competencias fundamentales en inteligencia artificial generativa y técnicas de prompt engineering.

Se enfatiza la comprensión de modelos de lenguaje (LLMs), sus capacidades, limitaciones y aplicaciones en contextos organizacionales. A lo largo de la experiencia, se analizan los principios de funcionamiento de los LLMs, diferenciando arquitecturas y evaluando aspectos como precisión, alucinación y eficiencia en el uso de tokens.

Se trabaja con APIs de modelos de lenguaje, explorando técnicas de redacción de prompts efectivos, incluyendo enfoques zero-shot, few-shot y chain-of-thought.

El enfoque práctico permite que las/los estudiantes desarrollen habilidades técnicas mediante la formulación de prompts optimizados para casos reales, fortaleciendo su pensamiento crítico para identificar y resolver requerimientos informacionales complejos en entornos organizacionales.

### Act 1.1 - Introducción a LLMs y Conexión API

**Indicadores de Logro:** IL1.1 - IL 1.2  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es comprender los fundamentos de los modelos de lenguaje y establecer conexiones básicas con APIs.

**Primera sesión (2 horas):** La/el docente realiza una introducción donde se describe la evolución de la IA hasta la generativa, presentando hitos históricos desde sistemas basados en reglas, pasando por machine learning tradicional, hasta llegar a los modelos generativos actuales. Se explican las arquitecturas fundamentales de LLMs: transformers, mecanismos de atención, y el concepto de pre-entrenamiento y fine-tuning. Se presentan las capacidades principales de los LLMs: generación de texto coherente, comprensión contextual, traducción, resumen, y razonamiento básico. También se abordan las limitaciones críticas: alucinaciones, sesgos inherentes, dependencia del contexto, y corte de conocimiento temporal. Las/los estudiantes configuran su entorno de desarrollo local instalando Python y las librerías necesarias (`groq`, `langchain-groq`, `requests`, `pandas`) con `uv sync`, y configuran su primer acceso a la API de Groq mediante su `GROQ_API_KEY` personal (verificable con `scripts/verify_groq.py`). Realizan sus primeras consultas básicas exploratorias utilizando Jupyter Notebook y analizan las respuestas obtenidas, documentando patrones iniciales observados.

**Segunda sesión (2 horas):** La/el docente profundiza en parámetros de configuración de APIs, explicando el impacto de temperatura (creatividad vs consistencia), max_tokens (longitud de respuesta), top_p (diversidad de vocabulario), frequency_penalty y presence_penalty (repetición de contenido). Se demuestra mediante ejemplos en vivo cómo cada parámetro afecta la calidad y variabilidad de las respuestas. Las/los estudiantes experimentan sistemáticamente con diferentes combinaciones de parámetros, comparando resultados para tareas específicas como generación creativa, respuestas técnicas precisas, y análisis de información. Practican la medición de tokens consumidos, calculan costos aproximados de uso, y establecen configuraciones base para diferentes tipos de consultas. Implementan casos de uso básicos: generación de contenido estructurado, resumen automático de textos, y sistemas básicos de preguntas y respuestas.

**Tercera sesión (2 horas):** La/el docente introduce conceptos de evaluación de LLMs, explicando métricas de precisión, detección de alucinaciones, y eficiencia en el uso de tokens. Se presentan técnicas básicas para validar respuestas y identificar inconsistencias. Las/los estudiantes desarrollan scripts para automatizar consultas repetitivas, implementan validaciones básicas de respuestas, y crean funciones reutilizables para diferentes tipos de interacciones con la API. Practican con casos de uso organizacionales reales: automatización de respuestas a consultas frecuentes, generación de reportes básicos, y procesamiento de información estructurada. Documentan las mejores prácticas identificadas, configuraciones óptimas para diferentes escenarios, y crean una guía de referencia personal para futuras implementaciones. Reflexionan grupalmente sobre las capacidades observadas, limitaciones identificadas, y potenciales aplicaciones en contextos profesionales.

**Actividades Trabajo Autónomo:**
- Configuración de entorno de desarrollo local
- Exploración adicional de documentación de APIs
- Práctica con diferentes tipos de consultas básicas

**Recursos de Aprendizaje:**
- 1.1.1 PPT Fundamentos de LLMs
- 1.1.2 Guía de Configuración API
- 1.1.3 Tutorial de Conexión Básica

**Tecnología Educativa:** Python, API Keys, Jupyter Notebook

**Bibliografía Obligatoria:** Hands-On Large Language Models, Cap.6, pp. 167-175

### Act 1.2 - Técnicas de Prompt Engineering

**Indicadores de Logro:** IL1.2 - IL 1.3  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es dominar técnicas avanzadas de formulación de prompts para optimizar respuestas de LLMs.

**Primera sesión (2 horas):** La/el docente presenta los fundamentos de prompt engineering, incluyendo principios de redacción efectiva: claridad, especificidad, estructura y contextualización. Se introducen las técnicas básicas de prompting: instrucciones directas, uso de delimitadores, y formateo de salida. Se explican los enfoques zero-shot (sin ejemplos previos) y few-shot (con ejemplos) mediante demostraciones comparativas. Las/los estudiantes practican la formulación de prompts para escenarios organizacionales básicos: generación de contenido estructurado, análisis de datos simples, y resolución de problemas específicos. Experimentan con diferentes estructuras de prompts y documentan la efectividad de cada enfoque.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas como chain-of-thought (razonamiento paso a paso) y role prompting (asignación de roles específicos). Se presentan estrategias para descomponer problemas complejos en pasos manejables y guiar el razonamiento del modelo. Las/los estudiantes implementan prompts que requieren análisis multifacético: evaluación de casos de negocio, análisis de tendencias de mercado, y diagnóstico de problemas técnicos. Practican la técnica de chain-of-thought para problemas que requieren razonamiento estructurado y documentan los patrones de éxito identificados.

**Tercera sesión (2 horas):** La/el docente introduce técnicas especializadas: prompt chaining (encadenamiento de prompts), system prompts (configuración de comportamiento), y técnicas de refinamiento iterativo. Se presentan métodos para evaluar la calidad de las respuestas y optimizar prompts basándose en resultados. Las/los estudiantes desarrollan flujos de trabajo complejos que combinan múltiples técnicas de prompting para resolver problemas organizacionales avanzados. Crean una biblioteca personal de templates de prompts efectivos para diferentes casos de uso y establecen métricas para evaluar su efectividad. Implementan un sistema de documentación que captura las mejores prácticas identificadas y las lecciones aprendidas durante la experimentación.

**Actividades Trabajo Autónomo:**
- Análisis comparativo de diferentes modelos LLM
- Investigación de métricas de evaluación específicas
- Documentación de criterios de selección de modelos

**Recursos de Aprendizaje:**
- 1.2.1 PPT Evaluación de LLMs
- 1.2.2 Guía de Métricas
- 1.2.3 Herramientas de Benchmarking

**Tecnología Educativa:** Python, API Keys, Jupyter Notebook, CodeGPT

**Bibliografía Obligatoria:** Hands-On Large Language Models, Cap.6, pp. 175-194

### Act 1.3 - Evaluación y Optimización de LLMs

**Indicadores de Logro:** IL1.4  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es desarrollar la capacidad de justificar decisiones de diseño en soluciones que integran LLMs y sistemas RAG, considerando aspectos técnicos, organizacionales y de trazabilidad.

**Primera sesión (2 horas):** La/el docente introduce marcos de trabajo para documentar y justificar arquitecturas que combinan LLMs con RAG, presentando metodologías para análisis de requerimientos organizacionales enfocados en gestión de conocimiento y criterios para selección de bases de datos vectoriales. Las/los estudiantes analizan casos organizacionales identificando fuentes de datos, requisitos de procesamiento, necesidades de indexación y restricciones presupuestarias, desarrollando matrices de decisión que justifican la selección de componentes (LLM, base vectorial, pipeline RAG) según requerimientos específicos del caso.

**Segunda sesión (2 horas):** La/el docente profundiza en metodologías para documentar decisiones técnicas en arquitecturas RAG incluyendo estrategias de chunking, selección de modelos de embedding, configuración de índices vectoriales y técnicas para evaluar limitaciones de cobertura y precisión. Las/los estudiantes desarrollan documentación técnica detallada que incluye diagramas de arquitectura RAG, flujos de procesamiento de datos, estrategias de actualización de índices, planes de monitoreo de calidad y análisis de costos operativos para sus casos organizacionales.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para documentación integral de soluciones RAG empresariales incluyendo arquitecturas de integración, políticas de gobierno de datos, estrategias de observabilidad y planes de escalabilidad. Las/los estudiantes desarrollan y presentan documentación completa que incluye justificación de arquitectura RAG, análisis de cumplimiento de SLAs, estrategias de mantenimiento, métricas de evaluación y plan de gestión de riesgos, defendiendo sus decisiones de diseño ante el grupo con argumentos técnicos y organizacionales sólidos.

**Actividades Trabajo Autónomo:**
- Análisis comparativo de diferentes modelos LLM
- Investigación de métricas de evaluación específicas
- Documentación de criterios de selección de modelos

**Recursos de Aprendizaje:**
- 1.3.1 PPT Evaluación de RAG y LLMs
- 1.3.2 Guía de Configuración de Base de datos Vectoriales y RAG
- 1.3.3 Herramientas de Benchmarking

**Tecnología Educativa:** Python, Herramientas de Evaluación, Dashboards

**Bibliografía Obligatoria:** Hands-On Large Language Models, Cap 8 pp. 225-258

### Evaluaciones EA 1

#### Ev For 1 - Quiz Fundamentos IA Generativa

**Indicadores de Logro:** IL1.1, IL1.2, IL1.3, IL1.4  
**Horas Docencia Directa:** 1 hrs  
**Horas Trabajo Autónomo:** 1 hrs  

Quiz obligatorio de 8 preguntas sobre conceptos fundamentales de IA generativa, arquitecturas de LLMs, técnicas de prompt engineering y evaluación de modelos. Las preguntas evalúan comprensión teórica de capacidades y limitaciones de LLMs, técnicas zero-shot, few-shot, chain-of-thought, y criterios de evaluación de precisión y eficiencia.

**Actividades Trabajo Autónomo:**
- Repaso de conceptos teóricos fundamentales
- Revisión de técnicas de prompt engineering
- Estudio de métricas de evaluación

#### Ev Parcial 1 - Diseño de Solución con LLM y RAG

**Indicadores de Logro:** IL1.1, IL1.2, IL1.3, IL1.4  
**Horas Docencia Directa:** 2 hrs (21 hrs)  
**Horas Trabajo Autónomo:** 1 hrs  

Proyecto integral donde los estudiantes analizan un caso organizacional, formulan prompts optimizados, diseñan e implementan pipeline RAG, construyen arquitectura de solución integrando LLMs con herramientas de recuperación, y documentan justificando decisiones de diseño. Se evalúa efectividad de prompts, implementación correcta de RAG, diseño de arquitectura y justificación fundamentada de decisiones.

**Actividades Trabajo Autónomo:**
- Estudio de arquitecturas RAG y pipelines de embeddings
- Recopilación de información del sector organizacional
- Investigación de técnicas de chunking
- Revisión de bibliografía sobre evaluación de precisión

---

## EA 2 - Desarrollo de Agentes Inteligentes con LLM

**Resultado de Aprendizaje:** RA2

**Descripción:**
En la segunda experiencia de aprendizaje, los estudiantes desarrollan competencias avanzadas en la construcción de agentes inteligentes basados en LLM.

Se enfatiza la comprensión del paradigma de agentes autónomos, la integración de herramientas externas, el manejo de memoria y las estrategias de planificación. A lo largo de la experiencia, se analizan arquitecturas de agentes LLM, diferenciando componentes como herramientas, memoria, planificación y ejecución.

Se trabaja con frameworks especializados para agentes, explorando function calling, integración con APIs y bases de datos, y protocolos como MCP. El enfoque práctico permite que los estudiantes construyan agentes funcionales que resuelvan tareas cognitivas complejas, fortaleciendo su capacidad para diseñar flujos de trabajo automatizados y documentar arquitecturas de sistemas inteligentes.

### Act 2.1 - Arquitectura y Frameworks de Agentes

**Indicadores de Logro:** IL2.1  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 8 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es comprender la arquitectura fundamental de agentes LLM y dominar frameworks especializados para construir agentes funcionales que integren herramientas de consulta, escritura y razonamiento.

**Primera sesión (2 horas):** La/el docente introduce el paradigma de agentes inteligentes explicando conceptos de autonomía, razonamiento y arquitectura básica (herramientas, memoria, planificación, ejecución), comparando diferentes enfoques arquitectónicos y presentando frameworks especializados como LangChain y CrewAI. Las/los estudiantes configuran su entorno de desarrollo, instalan frameworks de agentes, exploran documentación técnica, implementan su primer agente básico con capacidades de consulta simple, practican function calling básico con herramientas externas simuladas y documentan la arquitectura implementada reflexionando sobre capacidades y limitaciones observadas.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de integración de herramientas, explicando patrones de diseño para agentes multi-herramienta, estrategias de orquestación de tareas y metodologías para manejo de errores en cadenas de herramientas. Las/los estudiantes desarrollan agentes que integran múltiples herramientas de consulta (APIs, bases de datos, servicios web), implementan capacidades de escritura automatizada (generación de reportes, emails, documentos), configuran herramientas de razonamiento lógico y análisis, y prueban la interoperabilidad entre diferentes tipos de herramientas en flujos de trabajo simulados.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para diseño de agentes en contextos organizacionales específicos, incluyendo análisis de requerimientos, patrones de automatización empresarial y estrategias de validación de resultados en entornos simulados. Las/los estudiantes diseñan e implementan agentes especializados para casos organizacionales específicos (atención al cliente, análisis de datos, gestión de contenido), integran herramientas de consulta, escritura y razonamiento en flujos coherentes, validan el funcionamiento en escenarios simulados de automatización organizacional, y documentan el diseño completo incluyendo justificación de decisiones arquitectónicas y evaluación de capacidades del agente construido.

**Cuarta sesión (2 horas):** La/el docente facilita sesiones de presentación y evaluación cruzada donde los estudiantes demuestran sus agentes funcionales, explicando arquitectura, capacidades integradas y aplicabilidad organizacional. Las/los estudiantes presentan sus agentes desarrollados demostrando capacidades de consulta, escritura y razonamiento integradas, reciben retroalimentación de pares sobre funcionalidad y diseño, realizan pruebas cruzadas de agentes desarrollados por otros equipos, refinan sus implementaciones basándose en observaciones y feedback recibido, y consolidan documentación final incluyendo lecciones aprendidas y recomendaciones para mejoras futuras.

**Actividades Trabajo Autónomo:**
- Instalación y configuración de frameworks de agentes
- Exploración de documentación técnica de LangChain y CrewAI
- Práctica con ejemplos básicos de function calling

**Recursos de Aprendizaje:**
- 2.1.1 PPT Arquitectura de Agentes
- 2.1.2 Guía de Frameworks
- 2.1.3 Tutorial de Configuración
- Ejemplos de Código Base

**Tecnología Educativa:** Python, LLM Frameworks, APIs

**Bibliografía Obligatoria:** Introduction to Large Language Models with GPT & LangChain

### Act 2.2 - Memoria y Herramientas Externas

**Indicadores de Logro:** IL2.1, IL2.2  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es implementar sistemas de memoria y integrar herramientas externas en agentes, configurando procesos de memoria y recuperación de contexto para asegurar la continuidad de tareas en flujos prolongados.

**Primera sesión (2 horas):** La/el docente explica tipos de memoria (short-term y long-term), su importancia en la continuidad de tareas, técnicas de recuperación de contexto, estrategias de persistencia y presenta protocolos de integración como MCP para herramientas externas. Las/los estudiantes configuran sistemas básicos de memoria para sus agentes implementando almacenamiento de conversaciones, desarrollan mecanismos de recuperación de contexto histórico, integran herramientas externas simples usando APIs REST, prueban la persistencia de información entre sesiones y evalúan la efectividad de la memoria implementada documentando las configuraciones realizadas.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de gestión de memoria incluyendo estrategias de compresión de contexto, políticas de retención y eliminación de información, y metodologías para optimización de recuperación en flujos prolongados con múltiples tareas concurrentes. Las/los estudiantes implementan sistemas de memoria jerárquica con diferentes niveles de persistencia, desarrollan algoritmos de recuperación selectiva de contexto relevante, configuran políticas automáticas de gestión de memoria (limpieza, archivado, priorización), integran múltiples herramientas externas con gestión coordinada de contexto, y validan la continuidad efectiva en flujos de trabajo complejos y prolongados.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para integración avanzada de herramientas externas usando protocolos MCP y A2A, incluyendo manejo de errores, recuperación de fallos, y estrategias de sincronización entre agentes y sistemas externos en contextos organizacionales. Las/los estudiantes implementan integraciones robustas con bases de datos empresariales, servicios web y APIs especializadas, desarrollan sistemas de recuperación automática ante fallos de herramientas externas, configuran sincronización de contexto entre múltiples agentes colaborativos, prueban la continuidad de tareas en escenarios de alta complejidad con múltiples dependencias, y documentan arquitecturas de integración con análisis de rendimiento y confiabilidad.

**Cuarta sesión (2 horas):** La/el docente facilita evaluación integral de sistemas de memoria y herramientas implementados, presentando metodologías de testing para continuidad de tareas y criterios de evaluación de efectividad en flujos prolongados. Las/los estudiantes realizan pruebas exhaustivas de continuidad en flujos de trabajo prolongados y complejos, evalúan la efectividad de recuperación de contexto en diferentes escenarios de uso, optimizan configuraciones de memoria basándose en métricas de rendimiento observadas, presentan sus implementaciones demostrando capacidades de continuidad y recuperación, y consolidan documentación técnica incluyendo recomendaciones para configuración óptima de memoria y herramientas en contextos organizacionales específicos.

**Actividades Trabajo Autónomo:**
- Investigación de técnicas de persistencia de memoria
- Exploración de APIs y servicios externos para integración
- Práctica con protocolos MCP y A2A

**Recursos de Aprendizaje:**
- 2.2.1 PPT Sistemas de Memoria
- 2.2.2 Guía de Integración MCP
- 2.2.3 Tutorial de APIs
- Plantillas de Configuración

**Tecnología Educativa:** Python, Bases de Datos, APIs REST, MCP Protocol

**Bibliografía Obligatoria:**
- Introduction to Large Language Models with GPT & LangChain
- A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)

### Act 2.3 - Planificación y Orquestación

**Indicadores de Logro:** IL2.3, IL2.4  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es implementar estrategias de planificación y toma de decisiones dentro de agentes, ajustando el comportamiento del sistema ante tareas con múltiples etapas y condiciones cambiantes, y documentar la orquestación de componentes.

**Primera sesión (2 horas):** La/el docente presenta estrategias fundamentales de planificación en agentes incluyendo algoritmos de toma de decisiones, técnicas para manejo de tareas multi-etapa, metodologías de adaptación ante condiciones cambiantes y principios básicos de orquestación de componentes. Las/los estudiantes implementan algoritmos básicos de planificación en sus agentes configurando árboles de decisión simples, desarrollan flujos de trabajo secuenciales con múltiples etapas definidas, programan mecanismos básicos de detección de cambios en condiciones del entorno, prueban la capacidad de adaptación del agente ante escenarios variables predefinidos, y crean diagramas iniciales de arquitectura documentando la estructura básica de componentes y sus interacciones.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de planificación incluyendo algoritmos de planificación dinámica, estrategias de re-planificación automática, manejo de dependencias complejas entre tareas, y metodologías de orquestación distribuida para sistemas multi-agente. Las/los estudiantes implementan algoritmos de planificación adaptativa que modifican estrategias en tiempo real, desarrollan sistemas de priorización dinámica de tareas basados en condiciones cambiantes, configuran mecanismos de coordinación entre múltiples componentes del agente, integran sistemas de monitoreo continuo para detección automática de cambios contextuales, prueban la robustez del sistema ante interrupciones y cambios inesperados en flujos de trabajo, y refinan diagramas de arquitectura incluyendo flujos de decisión complejos y puntos de adaptación.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para documentación integral de sistemas de planificación y orquestación, incluyendo técnicas de modelado de comportamiento, estrategias de validación de decisiones, y estándares para documentación técnica de arquitecturas adaptativas en contextos organizacionales. Las/los estudiantes validan exhaustivamente el comportamiento de sus agentes en escenarios complejos con múltiples variables y condiciones cambiantes, optimizan algoritmos de planificación basándose en métricas de rendimiento y efectividad observadas, desarrollan documentación técnica completa incluyendo diagramas UML de comportamiento, especificaciones de algoritmos de decisión, y matrices de respuesta ante diferentes condiciones, presentan sus implementaciones demostrando capacidades de planificación adaptativa y toma de decisiones robusta, y consolidan documentación final con análisis de casos de uso, limitaciones identificadas y recomendaciones para implementación en entornos organizacionales reales.

**Actividades Trabajo Autónomo:**
- Estudio de algoritmos de planificación en IA
- Investigación de técnicas de orquestación de sistemas
- Práctica con herramientas de diagramación de arquitecturas

**Recursos de Aprendizaje:**
- 2.3.1 PPT Planificación de Agentes
- 2.3.2 Guía de Orquestación
- 2.3.3 Plantillas de Documentación
- Herramientas de Diagramación

**Tecnología Educativa:** Python, Herramientas de Modelado, Diagramas UML

**Bibliografía Obligatoria:**
- Introduction to Large Language Models with GPT & LangChain
- A survey of agent interoperability protocols: Model Context Protocol (MCP), Agent Communication Protocol (ACP), Agent-to-Agent Protocol (A2A), and Agent Network Protocol (ANP)

### Evaluaciones EA 2

#### Ev For 2 - Quiz Agentes de IA

**Indicadores de Logro:** IL2.1, IL2.2  
**Horas Docencia Directa:** 2 hrs  
**Horas Trabajo Autónomo:** 1 hrs  

Quiz obligatorio de 8 preguntas sobre conceptos fundamentales de agentes de IA. Las preguntas evalúan conocimientos teóricos sobre arquitectura de agentes LLM, frameworks, tipos de memoria, function calling, integración con herramientas externas y estrategias de planificación.

**Actividades Trabajo Autónomo:**
- Estudio de material teórico sobre paradigmas de agentes
- Revisión de documentación sobre frameworks
- Investigación de conceptos sobre function calling

#### Ev For 2 - Construcción de Agente Básico

**Indicadores de Logro:** IL2.1, IL2.2, IL2.3, IL2.4  
**Horas Docencia Directa:** 2 hrs (24 hrs)  
**Horas Trabajo Autónomo:** 2 hrs  

Los estudiantes construyen un agente básico que integre herramientas y memoria para resolver una tarea específica. Se evalúa la construcción de agentes funcionales con herramientas integradas y la configuración correcta de procesos de memoria para continuidad de tareas.

**Actividades Trabajo Autónomo:**
- Estudio de documentación técnica sobre implementación de agentes
- Recopilación de ejemplos de código

---

## EA 3 - Observabilidad, Seguridad y Ética en Agentes de IA

**Resultado de Aprendizaje:** RA3

**Descripción:**
En la tercera experiencia de aprendizaje, las/los estudiantes desarrollan competencias críticas en observabilidad, seguridad y consideraciones éticas para agentes de IA. Se enfatiza la implementación de herramientas de monitoreo, análisis de trazabilidad y aplicación de buenas prácticas éticas.

A lo largo de la experiencia, se analizan métricas de desempeño, técnicas de observabilidad y protocolos de seguridad. Se trabaja con herramientas especializadas de monitoreo, explorando análisis de logs, detección de anomalías y optimización basada en datos observados.

El enfoque práctico permite que las/los estudiantes implementen sistemas de observabilidad completos, fortaleciendo su capacidad para garantizar escalabilidad, seguridad y sostenibilidad en sistemas de agentes de IA en producción.

### Act 3.1 - Herramientas de Observabilidad

**Indicadores de Logro:** IL3.1  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 8 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es dominar herramientas de observabilidad para monitorear agentes de IA, aplicando métricas de observabilidad para medir la precisión, latencia y consistencia de un agente de IA en escenarios con variabilidad de datos.

**Primera sesión (2 horas):** La/el docente introduce conceptos fundamentales de observabilidad en agentes de IA explicando qué observar y por qué es crítico, presenta arquitecturas de monitoreo, define métricas clave (latencia, frecuencia de errores, uso de tokens, precisión), y explica metodologías para medición de consistencia. Las/los estudiantes configuran herramientas básicas de observabilidad en agentes existentes, implementan sistemas de captura de métricas fundamentales, configuran dashboards iniciales de monitoreo, y ejecutan pruebas básicas midiendo latencia y precisión en escenarios controlados.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de observabilidad incluyendo configuración de alertas automáticas, análisis de métricas complejas y metodologías para evaluación de consistencia en datos variables. Las/los estudiantes implementan dashboards avanzados con múltiples dimensiones de análisis, configuran alertas automáticas para detección de anomalías, desarrollan baterías de pruebas con variabilidad de datos, y analizan correlaciones entre diferentes métricas de rendimiento.

**Tercera sesión (2 horas):** La/el docente presenta estrategias para pruebas de estrés y escenarios de alta variabilidad, metodologías de benchmark y técnicas de optimización basadas en métricas. Las/los estudiantes implementan pruebas de carga y estrés en sus agentes, evalúan comportamiento bajo diferentes condiciones de variabilidad de datos, realizan benchmarking comparativo entre diferentes configuraciones, y documentan impacto de la variabilidad en el rendimiento del sistema.

**Cuarta sesión (2 horas):** La/el docente facilita el análisis integral de datos recolectados y presenta frameworks para toma de decisiones basada en observabilidad. Las/los estudiantes realizan análisis exhaustivo de métricas acumuladas, identifican patrones y tendencias en diferentes escenarios, proponen y validan optimizaciones específicas basadas en datos observados, y presentan hallazgos con evidencia cuantitativa del impacto de la variabilidad de datos en el rendimiento del agente.

**Actividades Trabajo Autónomo:**
- Configuración de herramientas de monitoreo adicionales
- Exploración de dashboards avanzados
- Investigación de métricas específicas por tipo de agente

**Recursos de Aprendizaje:**
- 3.1.1 PPT Observabilidad de Agentes
- 3.1.2 Guía de LangSmith
- 3.1.3 Tutorial de Métricas
- Plantillas de Dashboard

**Tecnología Educativa:** LangSmith, Langfuse, Arize, Dashboards

**Bibliografía Obligatoria:**
- Hands-On Large Language Models
- Introduction to Large Language Models with GPT & LangChain

### Act 3.2 - Análisis de Trazabilidad y Logs

**Indicadores de Logro:** IL3.2  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es desarrollar habilidades de análisis de registros de ejecución del agente, utilizando herramientas de trazabilidad para identificar puntos de falla o mejora en flujos automatizados.

**Primera sesión (2 horas):** La/el docente introduce conceptos fundamentales de análisis de logs y trazabilidad en agentes de IA, presenta técnicas básicas de análisis de registros de conversación, explica metodologías para identificación de patrones en flujos de ejecución, y demuestra el uso de herramientas básicas de visualización de trazas. Las/los estudiantes configuran sistemas de registro detallado en sus agentes, implementan captura de logs en puntos críticos del flujo de ejecución, analizan registros básicos de conversaciones identificando patrones comunes, y practican con herramientas de visualización para mapear flujos de decisión simples.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de análisis de trazabilidad, presenta metodologías para detección de anomalías en flujos complejos, explica estrategias para correlación de eventos en registros distribuidos, y demuestra técnicas de visualización avanzada de rutas de ejecución. Las/los estudiantes implementan análisis detallado de logs en flujos complejos, utilizan herramientas especializadas para seguimiento de decisiones del agente, identifican patrones de comportamiento anómalo en diferentes escenarios, y desarrollan mapas visuales de puntos críticos de falla en flujos automatizados.

**Tercera sesión (2 horas):** La/el docente presenta metodologías para análisis sistemático de fallas, técnicas de diagnóstico root-cause, estrategias para priorización de mejoras basadas en impacto, y frameworks para documentación de hallazgos y recomendaciones. Las/los estudiantes realizan análisis exhaustivo de logs problemáticos identificando causas raíz de fallas, desarrollan matrices de priorización para mejoras potenciales, documentan patrones de falla recurrentes con evidencia de logs, proponen optimizaciones específicas basadas en análisis de trazabilidad, y presentan reportes técnicos detallados con recomendaciones concretas para optimización de flujos automatizados.

**Actividades Trabajo Autónomo:**
- Análisis de casos de estudio de logs problemáticos
- Investigación de técnicas avanzadas de análisis de trazas
- Práctica con herramientas de visualización de flujos

**Recursos de Aprendizaje:**
- 3.2.1 PPT Análisis de Trazabilidad
- 3.2.2 Guía de Análisis de Logs
- 3.2.3 Herramientas de Visualización
- 3.2.4 Casos de Estudio

**Tecnología Educativa:** Herramientas de Análisis, Visualizadores de Logs, Trazabilidad

**Bibliografía Obligatoria:**
- Hands-On Large Language Models
- Introduction to Large Language Models with GPT & LangChain

### Act 3.3 - Seguridad, Ética y Escalabilidad

**Indicadores de Logro:** IL3.3, IL3.4  
**Ambiente de Aprendizaje:** Taller de Proyectos (Taite 7)  
**N° Estudiantes:** 30  
**Horas Docencia Directa:** 6 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

**Descripción Dirigida al Docente:**
El propósito de esta actividad es implementar protocolos de seguridad y uso responsable en el diseño de agentes, considerando aspectos éticos, normativos y de privacidad, mientras se desarrollan estrategias para mejorar el desempeño y escalabilidad de las soluciones.

**Primera sesión (2 horas):** La/el docente introduce fundamentos de seguridad en agentes de IA, presenta conceptos de guardrails y políticas de control, explica principios éticos fundamentales en IA (privacidad, transparencia, equidad), y describe mecanismos básicos de control de alucinaciones. Las/los estudiantes implementan controles de seguridad básicos en sus agentes, configuran políticas iniciales de protección de datos, desarrollan mecanismos de validación de respuestas, y documentan consideraciones éticas básicas en sus diseños.

**Segunda sesión (2 horas):** La/el docente profundiza en técnicas avanzadas de seguridad, presenta frameworks éticos específicos para IA, explica metodologías de detección y mitigación de sesgos, y describe estrategias de human-in-the-loop. Las/los estudiantes implementan sistemas avanzados de control de alucinaciones, desarrollan mecanismos de detección de sesgos, configuran flujos de supervisión humana, y evalúan impacto ético de sus soluciones en diferentes contextos.

**Tercera sesión (2 horas):** La/el docente presenta principios de escalabilidad y sostenibilidad en sistemas de IA, metodologías de optimización de recursos, estrategias de paralelización y técnicas de balanceo de carga. Las/los estudiantes analizan métricas de desempeño recolectadas, identifican cuellos de botella en sus implementaciones, diseñan estrategias de escalamiento horizontal y vertical, implementan mejoras de eficiencia basadas en datos observados, y documentan planes de optimización.

**Actividades Trabajo Autónomo:**
- Investigación de marcos éticos para IA
- Estudio de casos de sesgos en sistemas de IA
- Exploración de técnicas de escalabilidad en la nube

**Recursos de Aprendizaje:**
- 3.3.1 PPT Seguridad y Ética
- 3.3.2 Guía de Guardrails
- 3.3.3 Marco Ético para IA
- 3.3.4 Estrategias de Escalabilidad

**Tecnología Educativa:** Guardrails, Herramientas de Seguridad, Plataformas Cloud

**Bibliografía Obligatoria:**
- Hands-On Large Language Models
- Introduction to Large Language Models with GPT & LangChain

### Evaluaciones EA 3

#### Ev For 3 - Quiz Observabilidad y Trazabilidad

**Indicadores de Logro:** IL3.1, IL3.2  
**Horas Docencia Directa:** 2 hrs  
**Horas Trabajo Autónomo:** 2 hrs  

Quiz obligatorio de 8 preguntas sobre conceptos fundamentales de observabilidad y trazabilidad. Las preguntas evalúan conocimientos sobre métricas de observabilidad, herramientas de monitoreo, análisis de logs y técnicas de identificación de puntos de falla.

**Actividades Trabajo Autónomo:**
- Estudio de material teórico sobre métricas de observabilidad
- Revisión de documentación sobre análisis de logs
- Investigación de conceptos sobre trazabilidad

#### Ev Parcial 3 - Implementación de Observabilidad

**Indicadores de Logro:** IL3.1, IL3.2, IL3.3, IL3.4  
**Horas Docencia Directa:** 2 hrs (24 hrs)  
**Horas Trabajo Autónomo:** 2 hrs  

Proyecto integral donde los estudiantes implementan un sistema completo de observabilidad, analizan registros para identificar mejoras, integran protocolos de seguridad y ética, y proponen un plan de escalabilidad y sostenibilidad para agentes en producción.

**Actividades Trabajo Autónomo:**
- Estudio de documentación técnica sobre herramientas de observabilidad
- Recopilación de mejores prácticas en análisis de logs
- Investigación de herramientas de trazabilidad