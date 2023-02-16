#!/usr/bin/python3

"""
Create a basics routes and register the blueprint
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response, jsonify
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
corss = a = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def storage(exception):
    """a function thta call storage.close"""
    try:
        storage.close()
    except AttributeError:
        print("cant find the attribute close")


@app.errorhandler(404)
def page_not_found(exception):
    """ Function that return an error when a page is not found """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default=5000),
            threaded=True)
