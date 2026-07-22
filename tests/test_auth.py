def test_login_com_credenciais_validas_redireciona_para_agenda(client):
    response = client.post(
        "/login",
        data={"username": "teste", "password": "teste123"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/agenda"


def test_login_com_senha_invalida_retorna_para_login(client):
    response = client.post(
        "/login",
        data={"username": "teste", "password": "senha-errada"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Usu\u00e1rio ou senha incorretos".encode("utf-8") in response.data


def test_login_com_campos_vazios_nao_quebra_aplicacao(client):
    response = client.post(
        "/login",
        data={"username": "", "password": ""},
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_acesso_agenda_sem_login_redireciona(client):
    response = client.get("/agenda", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"] == "/login"