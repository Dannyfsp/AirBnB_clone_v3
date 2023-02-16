#!/usr/bin/python3

"""gettig the state object from databse"""
from models.base_model import *
from api.v1.views import app_views
from models import storage
from models.user import *
from flask import jsonify, abort, request, make_response


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    """Function that retrieve and save a new User"""
    ls = []
    users = storage.all('User').values()
    if request.method == "GET":
        for user in users:
            ls.append(user.to_dict())
        return jsonify(ls)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif 'email' not in request.json:
            return make_response(jsonify({'error': "Missing email"}), 400)
        elif 'password' not in request.json:
            return make_response(jsonify({'error': "Missing password"}), 400)
        else:
            new = User(**request.json)
            new.save()
            return make_response(new.to_dict(), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def RUD_users_byID(user_id):
    """get amenitiea by their ID
    it uses get,put and delete http method
    get will list a amenities obj
    put will update the city
    delete will remove the amenities"""
    user = storage.get(User, user_id)
    if request.method == "GET":
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        if not user:
            abort(404)
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == "PUT":
        if not user:
            abort(404)
        elif not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)

        else:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            user.updated_at = datetime.utcnow()
            storage.save()
            return make_response(jsonify(user.to_dict()), 200)
