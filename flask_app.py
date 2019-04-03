from flask import Flask, url_for, request, render_template, redirect, flash
import json
from database import *
from werkzeug.security import generate_password_hash, check_password_hash
import time

def init_content(content, width=4, height=5, page=1):
    count_pages = len(content) / width * height 
    count_pages += count_pages % 1 != 0

    new_content = list()
    for i in range(height):
        new_content.append(content[(page - 1) * width * height + i * width : (page - 1) * width * height + (i + 1) * width ])
    return new_content, int(count_pages)

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
        correct = User.query.filter(User.login == login).first()
        if not (login and password):
            error = "Одно из полей не заполнено"
        elif not check_password_hash(correct.password, password):
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
            password = generate_password_hash(password)
            user = User(password=password, login=login, admin=False)
            db.session.add(user)
            db.session.commit()
            correct = User.query.filter(User.login == login).first()
            session['username'] = correct.login
            session['user_id'] = correct.id
            session['admin'] = correct.admin
            return redirect('/')
        return render_template('registration.html', title=': Регистрация', fixed_footer=True, error=error)

@app.route('/add_film', methods=["GET", "POST"])
def admin():
    if session["admin"]:
        if request.method == "GET":
            return render_template("add_film.html")
        elif request.method == "POST":
            film = Film(name=request.form["name_film"],
                        description=request.form["description"],
                        url_bg_img=request.form["url_bg_img"],
                        genres=request.form["genres"].lower(), 
                        length=request.form['length'],
                        year=request.form["year"])
            db.session.add(film)
            db.session.commit()
            return render_template("add_film.html", title=": Фильм добавлен")
    else:
        return render_template("error_404.html", title=": Страница не найдена", fixed_footer=True)


@app.errorhandler(404)
def not_found(error):
    return render_template("error_404.html", title=": Страница не найдена", fixed_footer=True)

@app.route("/page/<int:nomb>")
def page(nomb):
    content, pages = init_content(Film.query.all())
    json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
    return render_template("main_page.html", corousel_content=json_list,
    genres_list=["Боевик", "Мелодрама", "Фентези"],
    page_link={"first": nomb == 1, "last": nomb == pages, "n_pages": list(range(1, pages))[nomb - 2:nomb + 2], "current": nomb},
    content=content)


# ---------------------------------------------

@app.route('/')
def main_page():
    nomb = 1
    content, pages = init_content(Film.query.all())
    json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
    return render_template("main_page.html", corousel_content=json_list,
    genres_list=["Боевик", "Мелодрама", "Фентези"],
    page_link={"first": nomb == 1, "last": nomb == pages, "n_pages": list(range(1, pages))[nomb - 2:nomb + 2], "current": nomb},
    content=content)
    


@app.route('/films/id<int:film_id>')
def film_page(film_id):
    return render_template('page_film.html')

@app.route('/user/id<int:user_id>')
def user_page(user_id):
    return render_template('profile.html', fixed_footer=True)

@app.route('/search/<name>')
def search_film(name):
    return

@app.route('/genres/<genre>')
def search_genres(ganre):
    return



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

