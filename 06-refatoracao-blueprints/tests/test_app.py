import pytest
from app import create_app

#hook
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    #O flask ele trabala sobre contexto, entao nao da para executar nada que esteja fora da
    # da aplicação. então os testes tem que estar no contexto da aplicação 
    context = app.app_context()
    context.push()

    yield app.test_client()

    context.pop()

def test_se_a_pagina_de_usuarios_retorna_status_code_200(client):
    response = client.get("/")
    assert response.status_code == 200

def test_se_o_link_de_registrar_existe(client):
    response = client.get("/")
    assert "Registrar" in response.get_data(as_text=True)

def test_se_o_link_de_login_existe(client):
    response = client.get("/")
    assert "Login" in response.get_data(as_text=True)


