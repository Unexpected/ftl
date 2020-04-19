import os
from demo import app as demo_app
from core import app as core_app
from werkzeug.exceptions import NotFound
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound(), {
    "/demo": demo_app,
    '/core': core_app
})


def check_system():
    print("App started at %s" % os.path.abspath('.'))


if __name__ == "__main__":
    check_system()
    app.run(debug=True)
