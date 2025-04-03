import psycopg2
from datetime import datetime
from utils import is_valid_email
import pytz 
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

class Users:
    def __init__(self, conn_database_crud_com_python):
        self.conn_database_crud_com_python = conn_database_crud_com_python
    
    def connect(self):
        return psycopg2.connect(**self.conn_database_crud_com_python)
    
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
                    
                    encrypt_password = self.encrypt_password(user_data['senha'])
                    data_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            
                    cur.execute("""
                                    INSERT INTO usuarios (nome, email, senha, data_criacao, data_atualizacao)
                                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                                """, 
                                (user_data['nome'], user_data['email'], encrypt_password, data_now, data_now))
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

                    for user in users:
                        user['senha'] = self.decrypt_password(user['senha'])

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

        if not user.get('email') or not is_valid_email(user['email']):
            return {"success": False, "message": "O campo 'email' é inválido."}

        if not user.get('senha') or not user['senha'].strip():
            return {"success": False, "message": "O campo 'senha' não pode estar vazio."}

        # Se todas as validações passarem
        return {"success": True, "message": "Validação bem-sucedida."}
    

    def encrypt_password(self, plain_password):
        return cipher_suite.encrypt(plain_password.encode('utf-8')).decode('utf-8')
    

    def decrypt_password(self, encrypted_password):
        return cipher_suite.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')
