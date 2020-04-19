from flask import Flask, request, make_response, current_app, g
from flask.json import jsonify
from db.database import reset, close_db, create_model
from db.database import get_entities, get_attributes, get_data
from db.database import insert_entity, get_modules, get_module
from flask_cors import CORS
from json_utils import Decoder, Encoder
import json
import time


app = Flask(__name__)
CORS(app)


@app.route('/engine/test')
# @with_appcontext
def test():
    print("will reset database")
    return "Test OK for engine !"


@app.route('/core/db/reset-db')
# @with_appcontext
def init_db_command():
    """Reset database."""
    print("will reset database")
    reset()
    print("database reset done !")
    return "OK"


@app.route('/core/db/create-model')
# @with_appcontext
def create_db_command():
    """Reset database."""
    data = create_model()
    return "OK"


def sqlalchemy_to_json(objects):
    dicts = [dict(o.__dict__) for o in objects]
    for d in dicts:
        del d["_sa_instance_state"]
    return jsonify([d for d in dicts])


@app.route('/api/core/modules')
def modules():
    modules = get_modules()
    return sqlalchemy_to_json(modules)


@app.route('/api/core/module/<module_name>')
def module(module_name):
    module = get_module(module_name)
    module_dict = module.__dict__
    entities_dict = dict()
    for e in module.entities:
        entity_dict = e.__dict__

        entities_dict[e.name] = entity_dict
        attributes_dict = dict()
        for a in e.attributes:
            attribute_dict = a.__dict__
            attributes_dict[a.name] = attribute_dict

            if "_sa_instance_state" in attribute_dict:
                del attribute_dict["_sa_instance_state"]
        entity_dict["attributes"] = attributes_dict
        if "_sa_instance_state" in entity_dict:
            del entity_dict["_sa_instance_state"]

    module_dict["entities"] = entities_dict
    del module_dict["_sa_instance_state"]
    # print(json.dumps(module_dict))
    # sqlalchemy_to_json([module])
    r = make_response(json.dumps(module_dict, indent=2))
    r.mimetype = 'application/json'
    return r


@app.route('/api/core/entities')
def entities():
    entities = get_entities()
    return sqlalchemy_to_json(entities)


@app.route('/api/core/data/<entity_name>')
def data(entity_name):
    entities = get_data(entity_name)
    return sqlalchemy_to_json(entities)


@app.route('/api/core/attributes/<entity_name>')
def attributes(entity_name):
    return sqlalchemy_to_json(get_attributes(entity_name))


@app.route('/api/core/person', methods=['POST'])
def create_person():
    print(request)
    print(request.data)
    return "OK"


def teardown(e):
    close_db()
    print("tearing down - %s" % e)


def after(response):
    print("after a request ? %s" % str(response)[:10])


def before_first():
    print("this is the first and only one call ?")


def before():
    print("before the request")


app.teardown_appcontext(teardown)
# app.after_request(after)
app.before_first_request(before_first)
app.before_request(before)
