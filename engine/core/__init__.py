from flask import Flask, g
from flask_cors import CORS

from core.db import check_db_connection, close_db_connection

app = Flask(__name__)
CORS(app)


@app.route("/")
def index_one():
    return "Hi im core"


@app.route('/test')
# @with_appcontext
def test():
    return "Test OK for core !"


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
