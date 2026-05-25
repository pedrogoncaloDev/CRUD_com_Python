import os 

if os.getenv("DEBUG") == "1":
    import debugpy

    debugpy.listen(("0.0.0.0", 5678))
    print("Aguardando debugger...")
    
    debugpy.wait_for_client()
    print("Debugger conectado, continuando execução...")


from flask import Flask, jsonify, request
from flask_cors import CORS
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
users = Users(CONN_DATABASE_USERHUB )

create_table_users()

# Rotas
@app.route('/users', methods=['POST'])
def create_user():
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
    try:
        user_deleted = users.delete_user(user_id)

        if user_deleted['success']:
            return jsonify({"message": user_deleted["message"]}), 200
        else:
            return jsonify({"error": user_deleted["message"]}), 400
    except Exception as e:
        return jsonify({"error": str(e)}),


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)