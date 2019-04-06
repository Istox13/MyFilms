from flask_sqlalchemy import SQLAlchemy
from flask import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = '/tmp'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

#column = db.Column('open', db.Boolean(), primary_key=False)
#add_column(db.engine, "User", column)


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    films = db.Column(db.String(50), unique=False, nullable=True)
    admin = db.Column(db.Boolean, unique=False, nullable=False)  
    open = db.Column(db.Integer, unique=False, nullable=False)  

    def __repr__(self):
        return '<User {} {} {} {}>'.format(
            self.id, self.login, self.password, self.open)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    url_bg_img = db.Column(db.String, unique=False, nullable=False)
    genres = db.Column(db.String, unique=False, nullable=False)
    coments = db.Column(db.String, unique=False, nullable=True)
    length = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)

db.create_all()