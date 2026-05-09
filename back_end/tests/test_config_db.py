from database.config_db import CONN_DATABASE_USERHUB

def test_CONN_DATABASE_USERHUB_structure():
    expected_keys = ["dbname", "user", "password", "host", "port"]
    assert set(CONN_DATABASE_USERHUB.keys()) == set(expected_keys)

def test_CONN_DATABASE_USERHUB_values():
    conn = CONN_DATABASE_USERHUB
    assert conn["dbname"] == "userhub"
    assert conn["user"] == "postgres"
    assert conn["password"] == "masterkey"
    assert conn["host"] == "host.docker.internal"
    assert conn["port"] == 5432
