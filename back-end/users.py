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
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM usuarios WHERE email = %s", (user['email'],))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já utilizado por outro usuário."}
            
                    # Converta as strings de data para objetos datetime
                    user['data_criacao'] = datetime.fromisoformat(user['data_criacao'].replace('Z', '+00:00'))
                    user['data_atualizacao'] = datetime.fromisoformat(user['data_atualizacao'].replace('Z', '+00:00'))
            
                    cur.execute("""
                                    INSERT INTO usuarios (nome, email, senha, data_criacao, data_atualizacao)
                                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                                """, 
                                (user['nome'], user['email'], user['senha'], user['data_criacao'], user['data_atualizacao']))
                    new_id = cur.fetchone()[0]

                    return {"success": True, "message": f"Usuário inserido com ID: {new_id}"}
        except Exception as e:
            return {"success": False, "message": f"{e}"}


    def read_users(self):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM usuarios order by id")

                    columns = [desc[0] for desc in cur.description]  # Obtém os nomes das colunas
                    users = [dict(zip(columns, line)) for line in cur.fetchall()]  # Converte cada linha em um dicionário
                
                    return {"success": True, "message": users}
        except Exception as e:
            return {"success": False, "message": f"{e}"}


    def update_user(self, user_data):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM usuarios WHERE id = %s", (user_data['id'],))
                    if not cur.fetchone():
                        return {"success": False, "message": "Usuário não encontrado."}
                    
                    cur.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (user_data['email'], user_data['id']))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já utilizado por outro usuário."}
                    
                    cur.execute("""
                                UPDATE usuarios
                                SET nome = %s, email = %s, senha = %s, data_atualizacao = %s
                                WHERE id = %s
                                """, 
                                (user_data['nome'], user_data['email'], user_data['senha'], user_data['data_atualizacao'], user_data['id'])
                                )
                    
                    return {"success": True, "message": f"Usuário com ID: {user_data['id']} atualizado com sucesso."}
        except Exception as e:
            return {"success": False, "message": f"{e}"}


    def delete_user(self, user_id):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))

                    return {"success": True, "message": f"Usuário com ID {user_id} deletado com sucesso."}
        except Exception as e:
            return {"success": False, "message": f"{e}"}
