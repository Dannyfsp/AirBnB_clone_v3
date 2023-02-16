#!/usr/bin/python3

"""gettig the state object from databse"""
from models import storage
from models.base_model import *
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.amenity import *
from models.state import State


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities():
    """Function that retrieve and save a new amenity"""
    ls = []
    amenities = storage.all('Amenity').values()
    if request.method == "GET":
        for amenity in amenities:
            ls.append(amenity.to_dict())
        return jsonify(ls)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif 'name' not in request.json:
            return make_response(jsonify({'error': "Missing name"}), 400)
        else:
            new = Amenity(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def get_amenities_byID(amenity_id):
    """get amenitiea by their ID
    it uses get,put and delete http method
    get will list a amenities obj
    put will update the city
    delete will remove the amenities"""
    amenity = storage.get(Amenity, amenity_id)
    if request.method == "GET":
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        if not amenity:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not amenity:
            abort(404)
        elif not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)

        else:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            city.updated_at = datetime.utcnow()
            storage.save()
            return make_response(jsonify(aemenity.to_dict()), 200)
