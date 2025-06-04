import psycopg2
from psycopg2 import sql
from config_db import conn_database_crud_com_python, conn_info

db_name = "crud_com_python"

def create_database():
    try:
        conn = psycopg2.connect(**conn_info)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if cur.fetchone():
                print(f"O banco de dados '{db_name}' já existe.")
            else:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Banco de dados '{db_name}' criado com sucesso.")
        finally:
            cur.close()
            conn.close()
    except psycopg2.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def create_table_users():
    try:
        conn = psycopg2.connect(**conn_database_crud_com_python)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_name = 'usuarios'
                );
            """)

            table_exists = cur.fetchone()[0]

            if table_exists:
                print("A tabela 'usuarios' já existe.")
            else:
                # Optei gerenciar manualmente os campos data_criacao e data_atualizacao via código Python ao invés de usar DEFAULT CURRENT_TIMESTAMP, como exercício prático de manipulação de datas e timestamps.
                cur.execute("""
                    CREATE TABLE usuarios (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(200) NOT NULL,
                        email VARCHAR(150) UNIQUE NOT NULL,
                        telefone VARCHAR(20) ,
                        data_criacao TIMESTAMP,
                        data_atualizacao TIMESTAMP
                    );
                """)

                print("Tabela 'usuarios' criada com sucesso.")

        finally:
            cur.close()
            conn.close()
    except psycopg2.Error as e:
        print(f"Erro ao criar a tabela 'usuarios': {e}")