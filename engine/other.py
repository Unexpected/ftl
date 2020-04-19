import sqlite3
import os
from flask import Flask, request, make_response
from flask import g

abspath = os.path.abspath('.')
DATABASE = 'sqlite/database.db'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def index():
    cur = get_db().cursor()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
