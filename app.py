from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

import hashlib

from mysql_config import MYSQL_CONFIG
app = Flask(__name__)
CORS(app)


app.config.update(MYSQL_CONFIG)
mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_pw)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(debug=True)
