from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="пароль",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = cursor.fetchall()
            if ' ' in str(username) or ' ' in str(password) or str(password) == "" or str(username) == "":
                return render_template('login.html', error="Неправильный логин или пароль, запрещены символы пробела")
            if len(records) == 0:
                return render_template('login.html', error="Нет такого пользователя")
            return render_template('account.html', full_name=records[0][1], username=username, password=password)
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        login = request.form.get('login').strip()
        password = request.form.get('password').strip()
        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())
        if len(records) != 0:
            return render_template('registration.html', error2="Данный пользователь уже зарегистрирован")
        records = list(cursor.fetchall())
        if "  " in str(name):
            return render_template('registration.html', error1="Лишние пробелы в Имени")
        elif str(name) == "":
            return render_template('registration.html', error1="Введено пустое имя пользователя")
        if " " in str(login):
            return render_template('registration.html', error2="Пробел недопустим")
        elif str(login) == "":
            return render_template('registration.html', error2="Введен пустой логин")
        if " " in str(password):
            return render_template('registration.html', error3="Пробел недопустим")
        elif str(password) == "":
            return render_template('registration.html', error3="Введен пустой пароль")
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')


if __name__ == "__main__":
    app.run(debug=True)