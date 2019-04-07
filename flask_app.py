from flask import Flask, url_for, request, render_template, redirect, flash
import json
from database import *
from werkzeug.security import generate_password_hash, check_password_hash
import time

def init_content(content, width=4, height=5, page=1):
    ln_cont = len(content)
    count_pages = ln_cont // (width * height )
    count_pages += (ln_cont % (width * height)) != 0

    new_content = list()
    for i in range(height):
        new_content.append(content[(page - 1) * width * height + i * width : 
        (page - 1) * width * height + (i + 1) * width ])
    

    if page in range(1, 4):
        pages = list(range(1, int(count_pages) + 1))[:5]
    elif page in range(int(count_pages) - 2, int(count_pages) + 1):
        pages = list(range(int(count_pages) - 5, int(count_pages) + 1))[-5:]
    elif not content:
        pages = [1]
    return new_content, pages, int(count_pages)

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
            user = User(password=password, login=login, admin=False, films=' ', open=1)
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


@app.route('/users_list', methods=["GET", "POST"])
def users_list():
    if session["admin"]:
        if request.method == "GET":
            users = User.query.all()
            return render_template("users_list.html", len_users=len(users), user_list=users, footer=1)
        elif request.method == "POST":
            if request.form.get('admin'):
                method = request.form["admin"][:2]
                user_id = int(request.form["admin"][2:])
                if method == 'up':
                    admin = True
                elif method == 'dn':
                    admin = False

                user = User.query.filter(User.id == user_id).first()
                user = User(password=user.password, login=user.login, 
                    admin=admin, 
                    films=user.films, 
                    id=user.id, open=user.open)
                User.query.filter(User.id == user_id).delete()
                db.session.add(user)
                db.session.commit()
                
            elif request.form.get('del'):
                User.query.filter_by(id = int(request.form["del"])).delete()
                db.session.commit()
                
            users = User.query.all()
            return render_template("users_list.html", title=": Операция выполнена", len_users=len(users), user_list=users, footer=1)
    else:
        return render_template("error_404.html", title=": Страница не найдена", fixed_footer=True)


@app.errorhandler(404)
def not_found(error):
    return render_template("error_404.html", title=": Страница не найдена", fixed_footer=True)


@app.route("/page/<int:nomb>", methods=["POST", "GET"])
def page(nomb):
    if request.method == "GET":
        content, pages, m_p = init_content(Film.query.all())
        json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
        return render_template("main_page.html", corousel_content=json_list,
        genres_list=["Боевик", "Мелодрама", "Фентези"],
        page_link={"first": nomb == 1, "tek_page": nomb, "last": nomb == m_p, "n_pages": pages, "current": nomb},
        content=content)
    elif request.method == "POST":
        return redirect(f"/search/{request.form['zapros']}/page1")
        


# ---------------------------------------------

@app.route('/')
def main_page():
    if request.method == "GET":
        nomb = 1 
        content, pages, m_p = init_content(Film.query.all())
        json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
        return render_template("main_page.html", corousel_content=json_list,
        genres_list=["Боевик", "Мелодрама", "Фентези"],
        page_link={"first": nomb == 1, "tek_page": nomb, "last": nomb == m_p, "n_pages": pages, "current": nomb},
        content=content)
    elif request.method == "POST":
        return redirect(f"/search/{request.form['zapros']}/page1")
    

@app.route('/user/id<int:user_id>', methods=["GET", "POST"])
def user_page(user_id):
    if request.method == "GET":
        user = User.query.filter(User.id == user_id).first()
        user_films = [Film.query.filter(Film.id == int(i)).first() for i in user.films.split()]

        ln_house = sum((int(i.length) for i in user_films)) / 60

        result = {
            "films": len(user_films),
            "hours": round(ln_house),
            "days": round(ln_house / 24)
        }
        return render_template('profile.html', fixed_footer=True, user_id=user_id, 
            private=User.query.filter(User.id == user_id).first().open,
            films_user=enumerate(user_films), title=': ' + user.login, footer=1,
            result=result)
    elif request.method == "POST":
        user = User.query.filter(User.id == user_id).first()
        user = User(password=user.password, login=user.login, 
            admin=user.admin, films=user.films, 
            id=user.id, open=(user.open + 1) % 2)
        User.query.filter(User.id == user_id).delete()
        db.session.add(user)
        db.session.commit()

        user_films = [Film.query.filter(Film.id == int(i)).first() for i in user.films.split()]
        
        ln_house = sum((int(i.length) for i in user_films)) / 60
        result = {
            "films": len(user_films),
            "hours": round(ln_house),
            "days": round(ln_house / 24)
        } 

        return render_template('profile.html', user_id=user_id, 
            private=User.query.filter(User.id == user_id).first().open,
            films_user=enumerate(user_films), footer=1, title=': ' + user.login,
            result=result)



@app.route('/films/id<int:film_id>', methods=["GET", "POST"])
def film_page(film_id):
    if request.method == "GET":
        film = Film.query.filter(Film.id == film_id).first()
        return render_template('page_film.html', film=film, 
            user=User.query.filter(User.id == session["user_id"]).first()  if "username" in session else None, 
            title=': ' + film.name)
    elif request.method == "POST":
        if "username" in session:
            user = User.query.filter(User.id == session["user_id"]).first()
            films = user.films.split()
            if str(film_id) in films:
                films = list(filter(lambda x: x != str(film_id), films))
            else:
                films = films + [str(film_id)]
            films = ' '.join(list(set(films)))
            user = User(password=user.password, login=user.login, 
                admin=user.admin, films=films, 
                id=user.id, open=user.open)
            User.query.filter(User.id == session["user_id"]).delete()
            db.session.add(user)
            db.session.commit()
        
        film = Film.query.filter(Film.id == film_id).first()

        return render_template('page_film.html', film=film, 
            user=User.query.filter(User.id == session["user_id"]).first() if "username" in session else None, 
            title=': ' + film.name)
        

@app.route('/genres/<genre>')
def search_genres(ganre):
    return



if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)

