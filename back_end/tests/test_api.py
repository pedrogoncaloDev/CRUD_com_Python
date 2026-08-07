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
    def test_sucesso_retorna_200_com_lista(self, client, mocker):
        test_client, users = client
        mocker.patch.object(
            users, "read_users", return_value={"success": True, "message": [{"id": 1, "nome": "Ana"}]}
        )

        response = test_client.get("/users")

        assert response.status_code == 200
        assert response.get_json() == [{"id": 1, "nome": "Ana"}]

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
