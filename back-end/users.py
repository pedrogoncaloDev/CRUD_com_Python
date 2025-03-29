import psycopg2
from datetime import datetime
from utils import is_valid_email
import pytz 

class Users:
    def __init__(self, conn_info):
        self.conn_info = conn_info
    
    def connect(self):
        return psycopg2.connect(**self.conn_info)
    
    def create_user(self, user_data):
        try:
            validate_user_data = self.validate_user(user_data)

            if not validate_user_data['success']:
                return validate_user_data
            
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM usuarios WHERE email = %s", (user_data['email'],))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já utilizado por outro usuário."}
                    
                    data_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            
                    cur.execute("""
                                    INSERT INTO usuarios (nome, email, senha, data_criacao, data_atualizacao)
                                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                                """, 
                                (user_data['nome'], user_data['email'], user_data['senha'], data_now, data_now))
                    new_id = cur.fetchone()[0]

                    return {"success": True, "message": f"Usuário inserido com ID: {new_id}"}
        except Exception as e:
            return {"success": False, "message": f"{e}"}


    def read_users(self):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM usuarios")

                    columns = [desc[0] for desc in cur.description]  # Obtém os nomes das colunas
                    users = [dict(zip(columns, line)) for line in cur.fetchall()]  # Converte cada linha em um dicionário

                    return {"success": True, "message": users}
        except Exception as e:
            return {"success": False, "message": f"{e}"}


    def update_user(self, user_data):
        try:
            validate_user = self.validate_user(user_data)
            
            if not validate_user['success']:
                return validate_user
            
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM usuarios WHERE id = %s", (user_data['id'],))
                    if not cur.fetchone():
                        return {"success": False, "message": "Usuário não encontrado."}
                    
                    cur.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", (user_data['email'], user_data['id']))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já utilizado por outro usuário."}
                    
                    data_atualizacao = datetime.utcnow().replace(tzinfo=pytz.UTC)
                    
                    cur.execute("""
                                UPDATE usuarios
                                SET nome = %s, email = %s, senha = %s, data_atualizacao = %s
                                WHERE id = %s
                                """, 
                                (user_data['nome'], user_data['email'], user_data['senha'], data_atualizacao, user_data['id'])
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


    def validate_user(self, user):
        if not user.get('nome') or not user['nome'].strip():
            return {"success": False, "message": "O campo 'nome' não pode estar vazio."}

        if not user.get('senha') or not user['senha'].strip():
            return {"success": False, "message": "O campo 'senha' não pode estar vazio."}

        if not user.get('email') or not is_valid_email(user['email']):
            return {"success": False, "message": "O campo 'email' é inválido."}

        # Se todas as validações passarem
        return {"success": True, "message": "Validação bem-sucedida."}
