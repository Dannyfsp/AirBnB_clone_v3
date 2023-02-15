#!/usr/bin/python3

"""
start a flask app
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def Get_status():
    """Get status , getting the status of ap and return json
    """
    return  jsonify({"status": "OK"})


