import importlib
from unittest.mock import MagicMock

import psycopg2
import pytest


@pytest.fixture
def mock_cursor():
    cursor = MagicMock()
    cursor.__enter__.return_value = cursor
    cursor.__exit__.return_value = False
    return cursor


@pytest.fixture
def mock_conn(mock_cursor):
    conn = MagicMock()
    conn.__enter__.return_value = conn
    conn.__exit__.return_value = False
    conn.cursor.return_value = mock_cursor
    return conn


@pytest.fixture
def mock_db(mocker, mock_conn):
    return mocker.patch("users.psycopg2.connect", return_value=mock_conn)


@pytest.fixture
def client(mocker):
    mocker.patch(
        "psycopg2.connect",
        side_effect=psycopg2.OperationalError("sem banco disponível durante os testes"),
    )

    import main

    importlib.reload(main)
    main.app.config.update(TESTING=True)

    with main.app.test_client() as test_client:
        yield test_client, main.users
