import pytest
from users import Users
from database.config_db import CONN_DATABASE_TEST_CRUD_COM_PYTHON

@pytest.fixture
def users():
    return Users(CONN_DATABASE_TEST_CRUD_COM_PYTHON)

def test_create_user(users):
    user_data = {
        "nome": "Usuário Teste",
        "email": "teste@example.com",
        "telefone": "11999999999"
    }
    result = users.create_user(user_data)
    assert result["success"] is True or "Email já utilizado" in result["message"]

def test_read_users(users):
    result = users.read_users()
    assert result["success"] is True
    assert isinstance(result["message"], list)