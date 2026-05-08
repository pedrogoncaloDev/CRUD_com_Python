import os

CONN_DATABASE_CRUD_COM_PYTHON = {
    "dbname": os.getenv("DB_CRUD_NAME"),
    "user": os.getenv("DB_CRUD_USER"),
    "password": os.getenv("DB_CRUD_PASSWORD"),
    "host": os.getenv("DB_CRUD_HOST"),
    "port": int(os.getenv("DB_CRUD_PORT", 5432)),
}

CONN_INFO = {
    "dbname": os.getenv("DB_DEFAULT_NAME"),
    "user": os.getenv("DB_DEFAULT_USER"),
    "password": os.getenv("DB_DEFAULT_PASSWORD"),
    "host": os.getenv("DB_DEFAULT_HOST"),
    "port": int(os.getenv("DB_DEFAULT_PORT", 5432)),
}