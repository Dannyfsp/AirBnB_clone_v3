#!/usr/bin/python3

"""gettig the state object from databse"""

from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.place import *
from models.city import City
from models.user import User
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def places_by_city(city_id):
    """Function that retrieve and save a new city"""
    places = storage.all('Place').values()
    city = storage.get(City, city_id)
    ls = []
    if city:
        for place in places:
            if place.city_id == city_id:
                ls.append(place.to_dict())
        if request.method == "GET":
            return jsonify(ls)
        elif request.method == "POST":
            if not request.json:
                return make_response(jsonify(
                                     {'error': "Not a JSON"}), 400)
            elif 'user_id' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing user_id"}), 400)
            elif 'name' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing name"}), 400)
            else:
                if storage.get(User, request.json['user_id']) is None:
                    abort(404)
                else:
                    json = request.json
                    json['city_id'] = city_id
                    new = Place(**json)
                    new.save()
                    return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def RUD_places_byID(amenity_id):
    """get amenitiea by their ID
    it uses get,put and delete http method
    get will list a amenities obj
    put will update the city
    delete will remove the amenities"""
    place = storage.get(Place, place_id)
    if request.method == "GET":
        if not place:
            abort(404)
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        if not place:
            abort(404)
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not place:
            abort(404)
        elif not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)

        else:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            place.updated_at = datetime.utcnow()
            storage.save()
            return make_response(jsonify(place.to_dict()), 200)
