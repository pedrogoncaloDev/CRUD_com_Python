import psycopg2
from psycopg2 import sql
from users import Users

conn_info = {
    'dbname': 'your_db_name',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'your_db_host',
    'port': 'your_db_port'
}

users = Users(conn_info)

test_user = {
    'nome': 'Test User',
    'email': 'testuser@example.com',
    'senha': 'password123',
    'data_criacao': '2025-01-03T23:57:32.225Z',
    'data_atualizacao': '2025-01-03T23:57:32.225Z'
}

print("Creating user...")
users.create_user(test_user)

print("Reading users...")
users.read_users()

print("Updating user...")
test_user = {
    'id': 1,
    'nome': 'Test User',
    'email': 'testuser@example.com',
    'senha': 'password123',
    'data_criacao': '2025-01-03T23:57:32.225Z',
    'data_atualizacao': '2025-01-03T23:57:32.225Z'
}
users.update_user(test_user)

print("Deleting user...")
users.delete_user(1)