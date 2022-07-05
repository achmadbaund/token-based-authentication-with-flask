from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS 
from bson import ObjectId
import json
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
bcrypt = Bcrypt(app)
secret = "***************"

mongo = MongoClient('localhost', 27017)
db = mongo['py_api'] #py_api is the name of the db

def tokenReq(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            try:
                jwt.decode(token, secret)
            except:
                return jsonify({"status": "fail", "message": "unauthorized"}), 401
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "fail", "message": "unauthorized"}), 401
    return decorated

@app.route('/')
def func():
    return "Hellow 😺", 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')