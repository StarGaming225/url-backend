from flask import Flask, request, jsonify
from flask_redis import FlaskRedis
from flask_cors import CORS

import random
import string

app = Flask(__name__)
CORS(app)
redis_client = FlaskRedis(app)

@app.route('/url/add', methods=["POST"])
def add_url():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    url = request.json.get('url')
    key = "".join([random.SystemRandom().choice(string.ascii_uppercase) for _ in range(20)])

    redis_client.set(key, url)
    return jsonify(key)

@app.route('/url/get', methods=["GET"])
def get_all_keys():
    all_keys = redis_client.keys("*")
    return jsonify([key.decode('utf-8') for key in all_keys])

@app.route('/url/get/<key>', methods=["GET"])
def get_key():
    grabbed_key = redis_client.get(key)
    return jsonify(grabbed_key.decode("utf-8"))


if __name__ == "__main__":
    app.run(debug=True)