import psycopg2
import pytest

from users import Users


@pytest.fixture
def users():
    return Users({"dbname": "test", "user": "test", "password": "test", "host": "localhost", "port": 5432})


@pytest.fixture
def valid_user_data():
    return {"nome": "Usuário Teste", "email": "teste@example.com", "telefone": "11987654321"}


class TestValidateUser:
    def test_dados_validos(self, users, valid_user_data):
        result = users.validate_user(valid_user_data)
        assert result == {"success": True, "message": "Validação bem-sucedida."}

    def test_nome_vazio(self, users, valid_user_data):
        valid_user_data["nome"] = "   "
        result = users.validate_user(valid_user_data)
        assert result == {"success": False, "message": "Nome completo não pode estar vazio."}

    def test_nome_ausente(self, users, valid_user_data):
        del valid_user_data["nome"]
        result = users.validate_user(valid_user_data)
        assert result["success"] is False

    def test_email_invalido(self, users, valid_user_data):
        valid_user_data["email"] = "email-invalido"
        result = users.validate_user(valid_user_data)
        assert result == {"success": False, "message": "Email inválido."}

    def test_telefone_com_tamanho_invalido(self, users, valid_user_data):
        valid_user_data["telefone"] = "123"
        result = users.validate_user(valid_user_data)
        assert result == {"success": False, "message": "Tamanho do número de telefone inválido"}

    def test_telefone_vazio_e_permitido(self, users, valid_user_data):
        valid_user_data["telefone"] = ""
        result = users.validate_user(valid_user_data)
        assert result == {"success": True, "message": "Validação bem-sucedida."}


class TestCreateUser:
    def test_dados_invalidos_nao_acessam_o_banco(self, users, mock_db, valid_user_data):
        valid_user_data["email"] = "invalido"

        result = users.create_user(valid_user_data)

        assert result["success"] is False
        mock_db.assert_not_called()

    def test_email_ja_utilizado(self, users, mock_db, mock_cursor, valid_user_data):
        mock_cursor.fetchone.return_value = (1,)

        result = users.create_user(valid_user_data)

        assert result == {"success": False, "message": "Email já utilizado por outro usuário."}

    def test_criacao_com_sucesso(self, users, mock_db, mock_cursor, valid_user_data):
        mock_cursor.fetchone.side_effect = [None, (42,)]

        result = users.create_user(valid_user_data)

        assert result == {"success": True, "message": "Usuário inserido com ID: 42"}

        insert_call = mock_cursor.execute.call_args_list[-1]
        insert_params = insert_call[0][1]
        assert insert_params[0] == valid_user_data["nome"]
        assert insert_params[1] == valid_user_data["email"]
        assert insert_params[2] == "11987654321"

    def test_erro_de_banco_de_dados_e_tratado(self, users, mock_db, mock_cursor, valid_user_data):
        mock_cursor.execute.side_effect = psycopg2.Error("falha ao inserir")

        result = users.create_user(valid_user_data)

        assert result["success"] is False
        assert "Erro de banco de dados" in result["message"]

    def test_erro_inesperado_e_tratado(self, users, mock_db, mock_cursor, valid_user_data):
        mock_cursor.execute.side_effect = ValueError("algo inesperado")

        result = users.create_user(valid_user_data)

        assert result == {"success": False, "message": "Erro inesperado: algo inesperado"}


class TestReadUsers:
    def test_retorna_lista_de_usuarios(self, users, mock_db, mock_cursor):
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.description = [
            ("id",), ("nome",), ("email",), ("data_criacao",), ("data_atualizacao",), ("telefone",)
        ]
        mock_cursor.fetchall.return_value = [(1, "Ana", "ana@example.com", None, None, "11987654321")]

        result = users.read_users()

        assert result == {
            "success": True,
            "message": {
                "users": [{
                    "id": 1,
                    "nome": "Ana",
                    "email": "ana@example.com",
                    "data_criacao": None,
                    "data_atualizacao": None,
                    "telefone": "11987654321",
                }],
                "total": 1,
                "page": 1,
                "per_page": 10,
            },
        }

    def test_retorna_lista_vazia_sem_usuarios(self, users, mock_db, mock_cursor):
        mock_cursor.fetchone.return_value = (0,)
        mock_cursor.description = []
        mock_cursor.fetchall.return_value = []

        result = users.read_users()

        assert result == {
            "success": True,
            "message": {"users": [], "total": 0, "page": 1, "per_page": 10},
        }

    def test_aplica_limit_e_offset_de_acordo_com_a_pagina(self, users, mock_db, mock_cursor):
        mock_cursor.fetchone.return_value = (0,)
        mock_cursor.description = []
        mock_cursor.fetchall.return_value = []

        users.read_users(page=3, per_page=20)

        select_call = mock_cursor.execute.call_args_list[-1]
        select_params = select_call[0][1]
        assert select_params == [20, 40]

    def test_sem_busca_nao_adiciona_where(self, users, mock_db, mock_cursor):
        mock_cursor.fetchone.return_value = (0,)
        mock_cursor.description = []
        mock_cursor.fetchall.return_value = []

        users.read_users()

        count_call = mock_cursor.execute.call_args_list[0]
        assert "WHERE" not in count_call[0][0]

    def test_busca_filtra_por_nome_email_telefone_ou_id(self, users, mock_db, mock_cursor):
        mock_cursor.fetchone.return_value = (0,)
        mock_cursor.description = []
        mock_cursor.fetchall.return_value = []

        users.read_users(search="ana")

        count_call = mock_cursor.execute.call_args_list[0]
        assert "WHERE" in count_call[0][0]
        assert count_call[0][1] == ["%ana%", "%ana%", "%ana%", "%ana%"]

        select_call = mock_cursor.execute.call_args_list[1]
        assert select_call[0][1] == ["%ana%", "%ana%", "%ana%", "%ana%", 10, 0]

    def test_erro_de_banco_de_dados_e_tratado(self, users, mock_db, mock_cursor):
        mock_cursor.execute.side_effect = psycopg2.Error("falha ao consultar")

        result = users.read_users()

        assert result["success"] is False
        assert "Erro de banco de dados" in result["message"]


class TestUpdateUser:
    @pytest.fixture
    def payload(self, valid_user_data):
        valid_user_data["id"] = 1
        return valid_user_data

    def test_usuario_nao_encontrado(self, users, mock_db, mock_cursor, payload):
        mock_cursor.fetchone.return_value = None

        result = users.update_user(payload)

        assert result == {"success": False, "message": "Usuário não encontrado."}

    def test_email_ja_utilizado_por_outro_usuario(self, users, mock_db, mock_cursor, payload):
        mock_cursor.fetchone.side_effect = [(1,), (2,)]

        result = users.update_user(payload)

        assert result == {"success": False, "message": "Email já utilizado por outro usuário."}

    def test_atualizacao_com_sucesso(self, users, mock_db, mock_cursor, payload):
        mock_cursor.fetchone.side_effect = [(1,), None]

        result = users.update_user(payload)

        assert result == {"success": True, "message": "Usuário com ID: 1 atualizado com sucesso."}

    def test_dados_invalidos_nao_acessam_o_banco(self, users, mock_db, payload):
        payload["nome"] = ""

        result = users.update_user(payload)

        assert result["success"] is False
        mock_db.assert_not_called()


class TestDeleteUser:
    def test_delecao_com_sucesso(self, users, mock_db):
        result = users.delete_user(1)

        assert result == {"success": True, "message": "Usuário com ID 1 deletado com sucesso."}

    def test_erro_na_delecao_e_tratado(self, users, mocker):
        mocker.patch("users.psycopg2.connect", side_effect=Exception("falha de conexão"))

        result = users.delete_user(1)

        assert result == {"success": False, "message": "falha de conexão"}
