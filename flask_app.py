from flask import Flask, url_for, request, render_template, redirect, flash
import json
from login import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def init_content(content, width=4, height=5):
    new_content = list()
    for i in range(height):
        new_content.append(content[i * width:(i + 1) * width])
    
    return new_content


@app.route('/')
def main_page():
    json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
    return render_template("main_page.html", corousel_content=json_list, 
    genres_list=["Боевик", "Милодрама", "Фентези"],
    page_link={"first": True, "last": False, "n_pages": range(1, 5), "current": 1},
    content=init_content([{"name": "Великая стена", "year": 2016, "id": 1, "length": 104, "headpiece": "https://www.kinopoisk.ru/images/film_big/611822.jpg"}] * 20))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title=': Вход', form=form, fixed_footer=True)

@app.route('/films/id<int:film_id>')
def test(film_id):
    return render_template('page_film.html')


@app.route('/registration')
def registration():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('registration.html', title=': Регистрация', form=form, fixed_footer=True)

'''@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

