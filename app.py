from flask import Flask, jsonify, request
from prometheus_client import Counter, start_http_server
import requests

# Create a Prometheus counter for HTTP requests
http_requests_total = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])


app = Flask(__name__)

# Expose Prometheus metrics on port 9100
start_http_server(9100)

orders = []

@app.route('/orders', methods=['GET'])
def get_orders():
    http_requests_total.labels(method='GET', endpoint='/orders').inc()  # Increment Prometheus counter
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    http_requests_total.labels(method='POST', endpoint='/orders').inc()  # Increment Prometheus counter
    user_id = request.json.get('user_id')
    
    # Use FQDN for the user-service in the same namespace
    user_response = requests.get(f'http://user-service.default.svc.cluster.local:5000/users/{user_id}')
    
    if user_response.status_code != 200:
        return jsonify({'error': 'User not found'}), 404
    
    new_order = {"id": len(orders) + 1, "user": user_response.json(), "item": "Item " + str(len(orders) + 1)}
    orders.append(new_order)
    return jsonify(new_order), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
