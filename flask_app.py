from flask import Flask, url_for, request, render_template, redirect
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def main_page():
    json_list = json.loads(open('static/json/carousel.json', "rt", encoding="utf8").read())
    print(json_list)
    return render_template("main_page.html", corousel_content=json_list, genres_list=["Боевик", "Милодрама", "Фентези"])

'''@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
