class TestCreateUserRoute:
    def test_sucesso_retorna_201(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users, "create_user", return_value={"success": True, "message": "Usuário inserido com ID: 1"}
        )

        response = test_client.post(
            "/users", json={"nome": "Ana", "email": "ana@example.com", "telefone": "11987654321"}
        )

        assert response.status_code == 201
        assert response.get_json() == {"message": "Usuário inserido com ID: 1"}

    def test_falha_de_validacao_retorna_400(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users, "create_user", return_value={"success": False, "message": "Email inválido."}
        )

        response = test_client.post("/users", json={"nome": "Ana", "email": "invalido", "telefone": ""})

        assert response.status_code == 400
        assert response.get_json() == {"error": "Email inválido."}

    def test_excecao_inesperada_retorna_400(self, client, mocker):
        test_client, users = client
        mocker.patch.object(users, "create_user", side_effect=Exception("falha inesperada"))

        response = test_client.post("/users", json={"nome": "Ana"})

        assert response.status_code == 400
        assert response.get_json() == {"error": "falha inesperada"}


class TestReadUsersRoute:
    def test_sucesso_retorna_200_com_pagina(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users,
            "read_users",
            return_value={
                "success": True,
                "message": {"users": [{"id": 1, "nome": "Ana"}], "total": 1, "page": 1, "per_page": 10},
            },
        )

        response = test_client.get("/users")

        assert response.status_code == 200
        assert response.get_json() == {"users": [{"id": 1, "nome": "Ana"}], "total": 1, "page": 1, "per_page": 10}
        users.read_users.assert_called_once_with(1, 10, None)

    def test_repassa_page_e_per_page_da_query_string(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users,
            "read_users",
            return_value={"success": True, "message": {"users": [], "total": 0, "page": 2, "per_page": 5}},
        )

        response = test_client.get("/users?page=2&per_page=5")

        assert response.status_code == 200
        users.read_users.assert_called_once_with(2, 5, None)

    def test_repassa_search_da_query_string(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users,
            "read_users",
            return_value={"success": True, "message": {"users": [], "total": 0, "page": 1, "per_page": 10}},
        )

        response = test_client.get("/users?search=ana")

        assert response.status_code == 200
        users.read_users.assert_called_once_with(1, 10, "ana")

    def test_falha_retorna_400(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users, "read_users", return_value={"success": False, "message": "Erro de banco de dados"}
        )

        response = test_client.get("/users")

        assert response.status_code == 400
        assert response.get_json() == {"error": "Erro de banco de dados"}


class TestUpdateUserRoute:
    def test_sucesso_retorna_201(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users,
            "update_user",
            return_value={"success": True, "message": "Usuário com ID: 1 atualizado com sucesso."},
        )

        response = test_client.put(
            "/users", json={"id": 1, "nome": "Ana", "email": "ana@example.com", "telefone": "11987654321"}
        )

        assert response.status_code == 201
        assert response.get_json() == {"message": "Usuário com ID: 1 atualizado com sucesso."}

    def test_usuario_nao_encontrado_retorna_400(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users, "update_user", return_value={"success": False, "message": "Usuário não encontrado."}
        )

        response = test_client.put("/users", json={"id": 999, "nome": "Ana"})

        assert response.status_code == 400
        assert response.get_json() == {"error": "Usuário não encontrado."}


class TestDeleteUserRoute:
    def test_sucesso_retorna_200(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users,
            "delete_user",
            return_value={"success": True, "message": "Usuário com ID 1 deletado com sucesso."},
        )

        response = test_client.delete("/users/1")

        assert response.status_code == 200
        assert response.get_json() == {"message": "Usuário com ID 1 deletado com sucesso."}

    def test_falha_retorna_400(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users, "delete_user", return_value={"success": False, "message": "Usuário não encontrado."}
        )

        response = test_client.delete("/users/1")

        assert response.status_code == 400
        assert response.get_json() == {"error": "Usuário não encontrado."}

    def test_excecao_inesperada_retorna_400(self, client, mocker):
        test_client, users = client
        mocker.patch.object(users, "delete_user", side_effect=Exception("falha inesperada"))

        response = test_client.delete("/users/1")

        assert response.status_code == 400
        assert response.get_json() == {"error": "falha inesperada"}
