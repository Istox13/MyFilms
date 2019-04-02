from flask import Flask, url_for, request, render_template, redirect, flash
import json
from login import LoginForm
from database import *


def init_content(content, width=4, height=5):
    new_content = list()
    for i in range(height):
        new_content.append(content[i * width:(i + 1) * width])
    
    return new_content

@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    session.pop('admin', 0)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', title=': Вход', fixed_footer=True)
    elif request.method == "POST":
        login = request.form["login"]
        password = request.form["u_password"]
        correct = User.query.filter(User.login == login, User.password == hash(password)).first()
        if not (login and password):
            error = "Одно из полей не заполнено"
        elif not correct:
            print(correct.password == hash(password))
            error = "Логин или пароль введены неверно"
        else:
            session['username'] = correct.login
            session['user_id'] = correct.id
            session['admin'] = correct.admin
            return redirect('/')
        return  render_template('login.html', title=': Вход', fixed_footer=True, error=error)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "GET":
        return render_template('registration.html', title=': Регистрация', fixed_footer=True)
    elif request.method == "POST":
        login = request.form["login"]
        password = request.form["u_password"]
        if not (login and password):
            error = "Одно из полей не заполнено"
        elif User.query.filter(User.login == login).first():
            error = "Данный логин уже занят"
        elif len(str(request.form["u_password"])) < 8:
            error = "В пароле меньше восьми символов"
        else:
            user = User(password=hash(password), login=login, admin=False)
            db.session.add(user)
            db.session.commit()
            correct = User.query.filter(User.login == login, User.password == hash(password)).first()
            session['username'] = correct.login
            session['user_id'] = correct.id
            session['admin'] = correct.admin
            return redirect('/')
        return render_template('registration.html', title=': Регистрация', fixed_footer=True, error=error)




@app.route('/')
def main_page():
    json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
    return render_template("main_page.html", corousel_content=json_list, 
    genres_list=["Боевик", "Мелодрама", "Фентези"],
    page_link={"first": True, "last": False, "n_pages": range(1, 5), "current": 1},
    content=init_content([{"name": "Великая стена", "year": 2016, "id": 1, "length": 104, "headpiece": "https://www.kinopoisk.ru/images/film_big/611822.jpg"}] * 20))

@app.route('/films/id<int:film_id>')
def film_page(film_id):
    return render_template('page_film.html')

@app.route('/user/id<int:user_id>')
def user_page(user_id):
    return render_template('page_film.html')

@app.route('/search/<name>')
def search_film(name):
    return

@app.route('/genres/<genre>')
def search_genres(ganre):
    return


'''@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

