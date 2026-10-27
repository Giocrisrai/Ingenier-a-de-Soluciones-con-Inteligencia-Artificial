"""Prueba los contratos de observabilidad de IL3.1 e IL3.2 sin llamar a Groq.

Los demos (`AgenteObservable.procesar`, `AgenteTrazable.procesar`) duermen y
fallan al azar: no sirven como prueba. Aquí se ejercita el recolector y el
analizador, que son lo que un informe de RA3 tiene que poder mostrar.
"""
import json

from cargar import cargar_modulo

obs = cargar_modulo("RA3/IL3.1/1-observability_tools.py")
trazas = cargar_modulo("RA3/IL3.2/1-traceability_analysis.py")


def test_resumen_vacio_no_divide_por_cero():
    assert obs.RecolectorMetricas().resumen() == {"total_peticiones": 0}


def test_resumen_calcula_latencia_tokens_y_tasa_de_error():
    recolector = obs.RecolectorMetricas()
    recolector.registrar(100, tokens_in=10, tokens_out=20, exitoso=True)
    recolector.registrar(300, tokens_in=5, tokens_out=0, exitoso=False)

    resumen = recolector.resumen()

    assert resumen["total_peticiones"] == 2
    assert resumen["tiempo_promedio_ms"] == 200
    assert resumen["tiempo_maximo_ms"] == 300
    assert resumen["tiempo_minimo_ms"] == 100
    assert resumen["total_tokens"] == 35
    assert resumen["tasa_errores_pct"] == 50


def test_traza_suma_etapas_y_conserva_el_texto_en_json():
    traza = trazas.Traza(trace_id="abc123", timestamp="t", mensaje_entrada="diseño")
    traza.agregar_evento("validacion_entrada", 0, 10.004, "ok", "Longitud: 6")
    traza.agregar_evento("generacion_respuesta", 10, 40, "error", "Timeout simulado")

    assert traza.duracion_total_ms() == 50.0
    data = json.loads(traza.a_json())
    assert data["trace_id"] == "abc123"
    assert data["mensaje_entrada"] == "diseño"
    assert data["eventos"][1]["estado"] == "error"
    assert data["eventos"][0]["duracion_ms"] == 10.0


def test_analizador_vacio():
    resumen = trazas.AnalizadorTrazas.resumir([])
    assert resumen["total_trazas"] == 0
    assert resumen["tasa_exito_pct"] == 0
    assert resumen["duracion_promedio_ms"] == 0


def test_analizador_separa_exito_error_y_promedio_por_etapa():
    ok = trazas.Traza(trace_id="ok", timestamp="t", mensaje_entrada="a")
    ok.agregar_evento("validacion_entrada", 0, 10, "ok")
    ok.agregar_evento("generacion_respuesta", 10, 30, "ok")

    error = trazas.Traza(trace_id="err", timestamp="t", mensaje_entrada="b")
    error.agregar_evento("validacion_entrada", 0, 20, "ok")
    error.agregar_evento("generacion_respuesta", 20, 40, "error", "timeout")

    resumen = trazas.AnalizadorTrazas.resumir([ok, error])

    assert resumen["total_trazas"] == 2
    assert resumen["trazas_con_error"] == 1
    assert resumen["tasa_exito_pct"] == 50.0
    assert resumen["duracion_promedio_ms"] == 50.0
    assert resumen["duracion_maxima_ms"] == 60.0
    assert resumen["promedio_por_etapa_ms"] == {
        "validacion_entrada": 15.0,
        "generacion_respuesta": 35.0,
    }
