from flask import Flask, request, jsonify
from users import Users
import psycopg2

app = Flask(__name__)

conn_info = {
    'dbname': 'crud_com_python',
    'user': 'postgres',
    'password': 'masterkey',
    'host': 'localhost',
    'port': '5432'
}

users = Users(conn_info)

@app.route('/users', methods=['GET'])
def read_users():
    all_users = users.read_users()
    return jsonify(all_users), 200

# @app.route('/users', methods=['POST'])
# def create_user():
#     user_data = request.json
#     users.create_user(user_data)
#     return jsonify({"message": "User created successfully"}), 201

# @app.route('/users/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
#     user_data = request.json
#     user_data['id'] = user_id
#     users.update_user(user_data)
#     return jsonify({"message": "User updated successfully"}), 200

# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     users.delete_user(user_id)
#     return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)