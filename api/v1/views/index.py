#!/usr/bin/python3

"""
start a flask app
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def Get_status():
    """Get status , getting the status of ap and return json
    """
    return  jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def Get_stat():
    """Get stat of each object, 
    getting the status of ap and return json
    """

    data = {"users": 'User', "states": 'State', "amenities": 'Amenity',
             "cities": 'City', "places": 'Place', "reviews": 'Review'}
    loadData = {}
    for key, value in data.items():
        loadData[key] = storage.count(value)
    return jsonify(loadData)
