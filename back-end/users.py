import psycopg2
from datetime import datetime
from utils import is_valid_email
import pytz

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
                    # Verifica email existente
                    cur.execute("SELECT id FROM usuarios WHERE email = %s", (user_data['email'],))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já utilizado por outro usuário."}

                    data_now = datetime.utcnow().replace(tzinfo=pytz.UTC)

                    cur.execute("""
                        INSERT INTO usuarios (nome, email, telefone, data_criacao, data_atualizacao)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id;
                    """, (user_data['nome'], user_data['email'], user_data['telefone'], data_now, data_now))
                    
                    new_id = cur.fetchone()[0]
                    conn.commit()

                    return {"success": True, "message": f"Usuário inserido com ID: {new_id}"}

        except psycopg2.Error as e:
            return {"success": False, "message": f"Erro de banco de dados: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {e}"}


    def read_users(self):
        try:
            with self.connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, nome, email, data_criacao, data_atualizacao, telefone FROM usuarios")
                    columns = [desc[0] for desc in cur.description]
                    users = []

                    for line in cur.fetchall():
                        user = dict(zip(columns, line))
                        users.append(user)

                    return {"success": True, "message": users}

        except psycopg2.Error as e:
            return {"success": False, "message": f"Erro de banco de dados: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {e}"}


    def update_user(self, user_data):
        try:
            validate_user = self.validate_user(user_data)
            if not validate_user['success']:
                return validate_user

            with self.connect() as conn:
                with conn.cursor() as cur:
                    # Verifica se usuário existe
                    cur.execute("SELECT id FROM usuarios WHERE id = %s", (user_data['id'],))
                    if not cur.fetchone():
                        return {"success": False, "message": "Usuário não encontrado."}

                    # Verifica email duplicado
                    cur.execute("SELECT id FROM usuarios WHERE email = %s AND id != %s", 
                               (user_data['email'], user_data['id']))
                    if cur.fetchone():
                        return {"success": False, "message": "Email já utilizado por outro usuário."}
                    
                    data_atualizacao = datetime.utcnow().replace(tzinfo=pytz.UTC)

                    cur.execute("""
                        UPDATE usuarios
                        SET nome = %s, email = %s, telefone = %s, data_atualizacao = %s
                        WHERE id = %s
                    """, (user_data['nome'], user_data['email'], user_data['telefone'], data_atualizacao, user_data['id']))
                    
                    conn.commit()
                    return {"success": True, "message": f"Usuário com ID: {user_data['id']} atualizado com sucesso."}

        except psycopg2.Error as e:
            return {"success": False, "message": f"Erro de banco de dados: {e}"}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {e}"}


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
        
        telefone_limpo = ''.join(filter(str.isdigit, str(user['telefone'])))

        if len(telefone_limpo) != 0:
            if len(telefone_limpo) != 11:
                return {"success": False, "message": "Telefone deve conter 11 dígitos (incluindo DDD)."}

        return {"success": True, "message": "Validação bem-sucedida."}