#!/usr/bin/python3

"""gettig the state object from databse"""
from models import storage
from models.base_model import *
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """
    this will use post and get method
    get - will list all the state
    post will addd to the state
    """
    all_state = storage.all('State').values()
    states_list = []
    if request.method == "GET":
        for state in all_state:
            states_list.append(state.to_dict())
        return jsonify(states_list)
    elif request.method == "POST":
        if not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)
        elif 'name' not in request.json:
            return make_response(jsonify({'error': "Missing name"}), 400)
        else:
            data = request.json
            loadData = State(**data)
            loadData.save()
            return make_response(loadData.to_dict(), 201)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def get_states_byID(state_id):
    """get state by their ID
    it uses get,put and delete http method
    get will list a state obj
    put will update the state
    delete will remove the state"""
    state = storage.get(State, state_id)
    if request.method == "GET":
        if not state:
            abort(404)

        return jsonify(state.to_dict())
    elif request.method == "DELETE":
        if not state:
            abort(404)
        storage.delete(state)
        storage.save()
    elif request.method == "PUT":
        if not state:
            abort(404)
        elif not request.json:
            return make_response(jsonify({'error': "Not a JSON"}), 400)

        else:
            data = request.get_json()
            print(data)
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
            state.updated_at = datetime.utcnow()
            storage.save()
            return make_response(jsonify(state.to_dict()), 200)
