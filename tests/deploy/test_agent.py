import agent


def test_modo_demo_sin_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    cliente = agent.AgentClient()
    assert cliente.modo_demo is True
    respuesta = cliente.responder("hola")
    assert "demo" in respuesta.lower()
    assert "hola" in respuesta.lower()


def test_detecta_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_falso")
    cliente = agent.AgentClient()
    assert cliente.modo_demo is False
