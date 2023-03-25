import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="пароль",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    error = "Неправильный логин или пароль, запрещены символы пробела"
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if ' ' in str(username):
        return render_template('login.html', error=error)
    if ' ' in str(password):
        return render_template('login.html', error=error)
    if len(records) == 0:
        return render_template('login.html', error1="Нет такого пользователя")
    return render_template('account.html', full_name=records[0][1], username=username, password=password)

if __name__ == "__main__":
    app.run(debug=True)