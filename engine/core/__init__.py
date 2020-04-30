import json

from flask import Flask, g, make_response
from flask_cors import CORS
from flask.json import jsonify

from core.model import *

from core.db import check_db_connection, close_db_connection, get_one, get_all, reset, get_module

app = Flask(__name__)
CORS(app)


@app.route("/")
def index_one():
    return "core API endpoint OK"


""" 
    /menu
    # tous les éléments de menu ? liste d'abord, arbre plus tard

    --> inner ref et backRef récupérées de façon unitaires
    --> récup cadrée par contexte

    / "custom" template ou "static"

    /
    Roots ? 


    Access == Demande d'un ensemble de données pour pouvoir afficher une vue
    Action == Validation d'un ensemble de trucs pour effectuer une "action métier"

    Rechercher un truc
    Travailler sur un truc
    Visualiser qqch de spécifique
    
"""


def sqlalchemy_to_json(objects):
    dicts = [dict(o.__dict__) for o in objects]
    for d in dicts:
        not_serializable = {"_sa_instance_state"}
        for attr in d:
            if callable(d[attr]) or isinstance(d[attr], (list, Entity)):
                not_serializable.add(attr)
        for to_remove in not_serializable:
            del d[to_remove]
    return jsonify([d for d in dicts])


@app.route('/query/<query_name>')
def query(query_name):
    """ List of all <entity_name> """
    all = get_all(query_name)
    main_entity = get_one("entity", query_name)
    pk = [k for k in main_entity.keys if k.key_type == 0][0]

    for e in all:
        _key_field_value = "-".join([e.__dict__[ka.attribute_name]
                                     for ka in pk.key_attributes])
        e.__dict__["_key_field_value"] = _key_field_value

    return sqlalchemy_to_json(all)


@app.route('/<entity_name>')
def all(entity_name):
    """ List of all <entity_name> """
    all = get_all(entity_name)
    return sqlalchemy_to_json(all)


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


@app.route('/<entity_name>/<primary_key>')
def one(entity_name, primary_key):
    """ List of all <entity_name> """
    if entity_name == "module":
        return module(primary_key)
    #e = get_one(entity_name, primary_key)
    return "NOT FOUND"  # sqlalchemy_to_json(all)


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
