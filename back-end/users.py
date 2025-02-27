import psycopg2
from psycopg2 import sql
from datetime import datetime

class Users:
    def __init__(self, conn_info):
        self.conn_info = conn_info
    
    def connect(self):
        return psycopg2.connect(**self.conn_info)
    
    def create_user(self, user):
        try:
            # Verifique se o email já existe
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM usuarios WHERE email = %s", (user['email'],))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já existe."}

            
            # Converta as strings de data para objetos datetime
            user['data_criacao'] = datetime.fromisoformat(user['data_criacao'].replace('Z', '+00:00'))
            user['data_atualizacao'] = datetime.fromisoformat(user['data_atualizacao'].replace('Z', '+00:00'))
            
            # Insira o usuário no banco de dados
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO usuarios (nome, email, senha, data_criacao, data_atualizacao)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """, (user['nome'], user['email'], user['senha'], user['data_criacao'], user['data_atualizacao']))
                    new_id = cur.fetchone()[0]

                    return {"success": True, "message": f"Usuário inserido com ID: {new_id}"}
        except Exception as e:
            return {"success": False, "message": f"{e}"}

    def read_users(self):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM usuarios")
                columns = [desc[0] for desc in cur.description]  # Obtém os nomes das colunas
                users = [dict(zip(columns, line)) for line in cur.fetchall()]  # Converte cada linha em um dicionário
                return users  # Retorna a lista de dicionários

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

    def delete_user(self, user_id):
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
                print(f"Usuário com ID {user_id} removido com sucesso.")