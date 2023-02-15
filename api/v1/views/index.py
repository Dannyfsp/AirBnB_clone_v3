#!/usr/bin/python3

"""
start a flask app
"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
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

