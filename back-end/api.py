from flask import Flask, jsonify, request
from users import Users
from config_db import conn_info
from utils import date_to_string
import json

app = Flask(__name__)
users = Users(conn_info)

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
            json_response = json.dumps(users_read['message'], default=date_to_string, indent=4)

            return json_response, 200
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
    app.run(debug=True)