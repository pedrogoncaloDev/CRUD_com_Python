import os

CONN_DATABASE_USERHUB = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

CONN_INFO = {
    "dbname": os.getenv("DB_DEFAULT_NAME"),
    "user": os.getenv("DB_DEFAULT_USER"),
    "password": os.getenv("DB_DEFAULT_PASSWORD"),
    "host": os.getenv("DB_DEFAULT_HOST"),
    "port": int(os.getenv("DB_DEFAULT_PORT", 5432)),
}