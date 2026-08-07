import os

if os.getenv("DEBUG") == "1":
	import debugpy

	debugpy.listen((os.getenv("DEBUG_HOST", "0.0.0.0"), int(os.getenv("DEBUG_PORT", 5678))))
	print("Aguardando debugger...")

	debugpy.wait_for_client()
	print("Debugger conectado, continuando execução...")


from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from users import Users
from database.config_db import CONN_DATABASE_USERHUB   # Corrigido o caminho do módulo
from database.database import create_table_users
import json

app = Flask(__name__)
CORS(app, resources={
	r"/*": {
		"origins": ["http://localhost:8080", "http://localhost:80"],
		"methods": ["GET", "POST", "PUT", "DELETE"],
		"allow_headers": ["Content-Type"]
	}
})

app.config['SWAGGER'] = {
	'title': 'UserHub API',
	'uiversion': 3,
	'specs_route': '/apidocs/'
}
swagger = Swagger(app, template={
	"swagger": "2.0",
	"info": {
		"title": "UserHub API",
		"description": "API REST para gerenciamento de usuários.",
		"version": "1.0.0"
	},
	"basePath": "/",
	"schemes": ["http"]
})

users = Users(CONN_DATABASE_USERHUB)

create_table_users()

# Rotas
@app.route('/users', methods=['POST'])
def create_user():
	"""Cria um novo usuário
	---
	tags:
	  - Users
	consumes:
	  - application/json
	parameters:
	  - in: body
	    name: body
	    required: true
	    schema:
	      type: object
	      required:
	        - nome
	        - email
	        - telefone
	      properties:
	        nome:
	          type: string
	          example: João da Silva
	        email:
	          type: string
	          example: joao@example.com
	        telefone:
	          type: string
	          example: "11987654321"
	responses:
	  201:
	    description: Usuário criado com sucesso
	    schema:
	      type: object
	      properties:
	        message:
	          type: string
	  400:
	    description: Dados inválidos ou email já utilizado
	    schema:
	      type: object
	      properties:
	        error:
	          type: string
	"""
	try:
		json_requisition = request.json
		user_created = users.create_user(json_requisition)

		if user_created['success']:
			return jsonify({"message": user_created["message"]}), 201
		else:
			return jsonify({"error": user_created["message"]}), 400
	except Exception as e:
		return jsonify({"error": str(e)}), 400


@app.route('/users', methods=['GET'])
def read_users():
	"""Lista todos os usuários
	---
	tags:
	  - Users
	responses:
	  200:
	    description: Lista de usuários
	    schema:
	      type: array
	      items:
	        type: object
	        properties:
	          id:
	            type: integer
	          nome:
	            type: string
	          email:
	            type: string
	          telefone:
	            type: string
	          data_criacao:
	            type: string
	            format: date-time
	          data_atualizacao:
	            type: string
	            format: date-time
	  400:
	    description: Erro ao buscar usuários
	    schema:
	      type: object
	      properties:
	        error:
	          type: string
	"""
	try:
		users_read = users.read_users()

		if users_read['success']:
			return jsonify(users_read['message']), 200
		else:
			return jsonify({"error": users_read["message"]}), 400
	except Exception as e:
		return jsonify({"error": str(e)}), 400


@app.route('/users', methods=['PUT'])
def update_user():
	"""Atualiza um usuário existente
	---
	tags:
	  - Users
	consumes:
	  - application/json
	parameters:
	  - in: body
	    name: body
	    required: true
	    schema:
	      type: object
	      required:
	        - id
	        - nome
	        - email
	        - telefone
	      properties:
	        id:
	          type: integer
	          example: 1
	        nome:
	          type: string
	          example: João da Silva
	        email:
	          type: string
	          example: joao@example.com
	        telefone:
	          type: string
	          example: "11987654321"
	responses:
	  201:
	    description: Usuário atualizado com sucesso
	    schema:
	      type: object
	      properties:
	        message:
	          type: string
	  400:
	    description: Dados inválidos, usuário não encontrado ou email já utilizado
	    schema:
	      type: object
	      properties:
	        error:
	          type: string
	"""
	try:
		user_data = request.json
		user_updated = users.update_user(user_data)

		if user_updated['success']:
			return jsonify({"message": user_updated["message"]}), 201
		else:
			return jsonify({"error": user_updated["message"]}), 400
	except Exception as e:
		return jsonify({"error": str(e)}), 400


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	"""Remove um usuário pelo ID
	---
	tags:
	  - Users
	parameters:
	  - in: path
	    name: user_id
	    type: integer
	    required: true
	    description: ID do usuário a ser removido
	responses:
	  200:
	    description: Usuário removido com sucesso
	    schema:
	      type: object
	      properties:
	        message:
	          type: string
	  400:
	    description: Erro ao remover usuário
	    schema:
	      type: object
	      properties:
	        error:
	          type: string
	"""
	try:
		user_deleted = users.delete_user(user_id)

		if user_deleted['success']:
			return jsonify({"message": user_deleted["message"]}), 200
		else:
			return jsonify({"error": user_deleted["message"]}), 400
	except Exception as e:
		return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
	app.run(host=os.getenv("FLASK_HOST", "127.0.0.1"), port=int(os.getenv("FLASK_PORT", 5000)))
