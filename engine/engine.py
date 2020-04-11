from flask import Flask, request, make_response
from flask.json import jsonify
from db.database import reset, close_db, create_model
from db.database import get_entities, get_attributes
from db.database import insert_entity, get_modules, get_module
from flask_cors import CORS
from json_utils import Decoder, Encoder
import json
import time

app = Flask(__name__)
CORS(app)


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
    entities_dict = []
    for e in module.entities:
        entity_dict = e.__dict__

        if "_sa_instance_state" in entity_dict:
            del entity_dict["_sa_instance_state"]
        entities_dict.append(entity_dict)
    module_dict["entities"] = entities_dict
    del module_dict["_sa_instance_state"]
    print(json.dumps(module_dict))
    # sqlalchemy_to_json([module])
    r = make_response(json.dumps(module_dict, indent=2))
    r.mimetype = 'application/json'
    return r


@app.route('/api/core/entities')
def entities():
    entities = get_entities()
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


app.teardown_appcontext(teardown)
