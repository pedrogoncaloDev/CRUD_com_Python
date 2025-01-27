import psycopg2
from psycopg2 import sql

class Users:
    def __init__(self, conn_info):
        self.conn_info = conn_info
    
    def connect(self):
        return psycopg2.connect(**self.conn_info)
    
    # CREATE - Adiciona um novo usuário
    def create_user(self, user):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO usuarios (nome, email, senha, data_criacao, data_atualizacao)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (user['nome'], user['email'], user['senha'], user['data_criacao'], user['data_atualizacao']))
                new_id = cur.fetchone()[0]
                print(f"Usuário inserido com ID: {new_id}")

    # READ - Obtem todos os usuários
    def read_users(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuarios")
                usuarios = cur.fetchall()
                for user in usuarios:
                    print(user)

    # UPDATE - Atualiza um usuário pelo ID
    def update_user(self, user_data):
        user_id = user_data.pop('id', None)
        if user_id is None:
            raise ValueError("user_data must contain 'id' key")

        with self.connect() as conn:
            with conn.cursor() as cur:
                updates = {k: v for k, v in user_data.items() if v is not None}
                
                set_clause = ", ".join(f"{key} = %s" for key in updates.keys())
                values = list(updates.values()) + [user_id]
                
                cur.execute(sql.SQL(f"UPDATE usuarios SET {set_clause} WHERE id = %s"), values)
                print(f"Usuário com ID {user_id} atualizado com sucesso.")

    # DELETE - Remove um usuário pelo ID
    def delete_user(self, user_id):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
                print(f"Usuário com ID {user_id} removido com sucesso.")
