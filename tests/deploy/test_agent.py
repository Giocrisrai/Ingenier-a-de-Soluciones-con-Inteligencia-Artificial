import agent


def test_modo_demo_sin_token(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    cliente = agent.AgentClient()
    assert cliente.modo_demo is True
    respuesta = cliente.responder("hola")
    assert "demo" in respuesta.lower()
    assert "hola" in respuesta.lower()


def test_detecta_token(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gsk_falso")
    cliente = agent.AgentClient()
    assert cliente.modo_demo is False
