"""Prueba las piezas de IL3.3 que sí tienen un contrato comprobable.

El filtro ético de ese script es un substring didáctico (bloquea «farmacia»
porque contiene «arma»). La versión que hay que defender es la de
`deploy/backend/guardrails.py`, cubierta en tests/deploy/. Aquí se prueba lo
que ese script añade y el despliegue no repite: la calculadora con AST y el
límite de tasa.
"""
from cargar import cargar_modulo

seguridad = cargar_modulo("RA3/IL3.3/1-security_ethics.py")


def test_evalua_aritmetica_simple():
    assert seguridad.evaluar_matematica_segura("(2 + 3) * 4") == "20"
    assert seguridad.evaluar_matematica_segura("2 ** 3") == "8"


def test_rechaza_codigo_que_no_es_aritmetica():
    for expresion in (
        "__import__('os').getcwd()",
        "(1).__class__",
        "abierta(",
        "",
    ):
        resultado = seguridad.evaluar_matematica_segura(expresion)
        assert resultado.startswith("Error"), expresion


def test_division_por_cero_no_revienta():
    assert seguridad.evaluar_matematica_segura("1/0").startswith("Error")


def test_limitador_corta_y_la_ventana_vuelve_a_abrir(monkeypatch):
    reloj = {"t": 1_000.0}
    monkeypatch.setattr(seguridad.time, "time", lambda: reloj["t"])
    limite = seguridad.LimitadorTasa(max_peticiones=1, ventana_segundos=10)

    assert limite.permitir() is True
    assert limite.permitir() is False
    assert limite.peticiones_restantes() == 0

    reloj["t"] = 1_011.0
    assert limite.permitir() is True
    assert limite.peticiones_restantes() == 0
