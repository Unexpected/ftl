from flask import Flask, g
from flask_cors import CORS
from flask.json import jsonify

from core.db import check_db_connection, close_db_connection, get_all, reset

app = Flask(__name__)
CORS(app)


@app.route("/")
def index_one():
    return "core API endpoint OK"


def sqlalchemy_to_json(objects):
    dicts = [dict(o.__dict__) for o in objects]
    for d in dicts:
        del d["_sa_instance_state"]
    return jsonify([d for d in dicts])


@app.route('/<entity_name>')
def all(entity_name):
    """ List of all <entity_name> """
    all = get_all(entity_name)
    return sqlalchemy_to_json(all)


@app.route('/db/reset-db')
# @with_appcontext
def init_db_command():
    """Reset database."""
    print("will reset database")
    reset()
    print("database reset done !")
    return "Database reset OK"


def teardown(e):
    # close_db()
    print("tearing down")


def after(response):
    print("Closing database connection")
    close_db_connection()
    return response


def before_first():
    print("Check core Database connection")
    check_db_connection()


def before():
    pass


app.teardown_appcontext(teardown)
app.after_request(after)
app.before_first_request(before_first)
app.before_request(before)

if __name__ == "__main__":
    app.run()
