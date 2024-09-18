from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = []

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json.get('user_id')
    user_response = requests.get(f'http://user-service:5000/users/{user_id}')
    
    if user_response.status_code != 200:
        return jsonify({'error': 'User not found'}), 404
    
    new_order = {"id": len(orders) + 1, "user": user_response.json(), "item": "Item " + str(len(orders) + 1)}
    orders.append(new_order)
    return jsonify(new_order), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
