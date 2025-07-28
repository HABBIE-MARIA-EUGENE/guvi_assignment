from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

import hashlib

from mysql_config import MYSQL_CONFIG
app = Flask(__name__)
CORS(app)


app.config.update(MYSQL_config)
mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    