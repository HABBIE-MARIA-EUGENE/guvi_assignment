from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import hashlib
import uuid

from redis_session import r  # Connects to Redis Cloud
from mysql_config import MYSQL_CONFIG

app = Flask(__name__)
CORS(app)

app.config.update(MYSQL_CONFIG)
mysql = MySQL(app)


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/profile', methods=['GET'])
def profile_page():
    return render_template('profile.html')



@app.route('/api/register', methods=['POST'])
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

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM users WHERE email=%s AND password=%s", (email, hashed_pw))
    user = cur.fetchone()
    cur.close()

    if user:
        token = str(uuid.uuid4())
        r.set(token, user[0])
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/api/profile', methods=['POST'])
def get_profile():
    token = request.json.get('token')
    user_id = r.get(token)

    if not user_id:
        return jsonify({"error": "Invalid or expired session"}), 403

    cur = mysql.connection.cursor()
    cur.execute("SELECT username, email, age, dob, contact FROM users WHERE id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        return jsonify({
            "username": user[0],
            "email": user[1],
            "age": user[2],
            "dob": str(user[3]) if user[3] else None,
            "contact": user[4]
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    token = data.get('token')
    age = data.get('age')
    dob = data.get('dob')
    contact = data.get('contact')

    user_id = r.get(token)
    if not user_id:
        return jsonify({"error": "Invalid session"}), 403

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET age=%s, dob=%s, contact=%s WHERE id=%s", (age, dob, contact, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Profile updated successfully"})


print("Registered routes:", app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
