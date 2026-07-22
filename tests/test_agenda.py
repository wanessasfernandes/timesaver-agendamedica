def login(client):
    return client.post(
        "/login",
        data={"username": "teste", "password": "teste123"},
    )


def test_api_agendamentos_retorna_dados_quando_autenticado(client):
    login(client)
    response = client.get("/api/agendamentos")

    assert response.status_code == 200
    dados = response.get_json()
    assert len(dados) == 1
    assert dados[0]["paciente"] == "Maria Souza"


def test_api_agendamentos_sem_login_e_bloqueada(client):
    response = client.get("/api/agendamentos", follow_redirects=False)

    assert response.status_code == 302


def test_busca_paciente_existente_retorna_resultado(client):
    login(client)
    response = client.get("/api/agendamentos?busca=Maria")

    dados = response.get_json()
    assert len(dados) == 1
    assert dados[0]["cpf"] == "123.456.789-00"


def test_busca_paciente_inexistente_retorna_lista_vazia(client):
    login(client)
    response = client.get("/api/agendamentos?busca=NomeQueNaoExiste")

    assert response.status_code == 200
    assert response.get_json() == []