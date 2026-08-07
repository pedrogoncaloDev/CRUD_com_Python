import importlib

from database import config_db


class TestConnDatabaseUserhub:
    def test_possui_todas_as_chaves_esperadas(self):
        expected_keys = {"dbname", "user", "password", "host", "port"}
        assert set(config_db.CONN_DATABASE_USERHUB.keys()) == expected_keys

    def test_le_valores_das_variaveis_de_ambiente(self, monkeypatch):
        monkeypatch.setenv("DB_NAME", "userhub_test")
        monkeypatch.setenv("DB_USER", "test_user")
        monkeypatch.setenv("DB_PASSWORD", "test_pass")
        monkeypatch.setenv("DB_HOST", "test_host")
        monkeypatch.setenv("DB_PORT", "5433")

        importlib.reload(config_db)

        assert config_db.CONN_DATABASE_USERHUB == {
            "dbname": "userhub_test",
            "user": "test_user",
            "password": "test_pass",
            "host": "test_host",
            "port": 5433,
        }

    def test_usa_valores_padrao_quando_host_e_port_nao_definidos(self, monkeypatch):
        monkeypatch.delenv("DB_HOST", raising=False)
        monkeypatch.delenv("DB_PORT", raising=False)

        importlib.reload(config_db)

        assert config_db.CONN_DATABASE_USERHUB["host"] == "localhost"
        assert config_db.CONN_DATABASE_USERHUB["port"] == 5432
