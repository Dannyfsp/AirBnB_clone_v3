#!/usr/bin/python3

"""
Create a basics routes and register the blueprint
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def storage(error):
    """a function thta call storage.close"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default=5000),
            threaded=True)
