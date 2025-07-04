from database.config_db import CONN_DATABASE_CRUD_COM_PYTHON, CONN_INFO

def test_conn_database_crud_com_python_structure():
    expected_keys = ["dbname", "user", "password", "host", "port"]
    assert set(config_db.CONN_DATABASE_CRUD_COM_PYTHON.keys()) == expected_keys

def test_conn_database_crud_com_python_values():
    conn = config_db.CONN_DATABASE_CRUD_COM_PYTHON
    assert conn["dbname"] == "crud_com_python"
    assert conn["user"] == "postgres"
    assert conn["password"] == "masterkey"
    assert conn["host"] == "host.docker.internal"
    assert conn["port"] == 5432

def test_conn_info_structure():
    expected_keys = ["dbname", "user", "password", "host", "port"]
    assert set(config_db.CONN_INFO.keys()) == expected_keys

def test_conn_info_values():
    conn = config_db.CONN_INFO
    assert conn["dbname"] == "postgres"
    assert conn["user"] == "postgres"
    assert conn["password"] == "masterkey"
    assert conn["host"] == "host.docker.internal"
    assert conn["port"] == 5432
