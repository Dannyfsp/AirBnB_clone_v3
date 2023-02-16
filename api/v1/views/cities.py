#!/usr/bin/python3

"""gettig the state object from databse"""
from models import storage
from models.base_model import *
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.city import *
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def cities_by_state(state_id):
    """Function that retrieve and save a new City"""
    state = storage.get(State, state_id)
    cities = storage.all('City').values()
    ls = []
    if state:
        for city in cities:
            if city.state_id == state_id:
                ls.append(city.to_dict())
        if request.method == "GET":
            return jsonify(ls)
        elif request.method == "POST":
            if not request.json:
                return make_response(jsonify(
                                     {'error': "Not a JSON"}), 400)
            elif 'name' not in request.json:
                return make_response(jsonify(
                                     {'error': "Missing name"}), 400)
            else:
                json = request.json
                json['state_id'] = state_id
                new = City(**json)
                new.save()
                return make_response(new.to_dict(), 201)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_cities_byID(city_id):
    """get city by their ID
    it uses get,put and delete http method
    get will list a city obj
    put will update the city
    delete will remove the city"""
    city = storage.get(City, city_id)
    if request.method == "GET":
        if not city:
            abort(404)
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not city:
            abort(404)
        elif not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)

        else:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(city, key, value)
            city.updated_at = datetime.utcnow()
            storage.save()
            return make_response(jsonify(city.to_dict()), 200)
