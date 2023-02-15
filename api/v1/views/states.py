#!/usr/bin/python3

"""gettig the state object from databse"""
import requests
from models import storage
from flask import jsonify
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    all_state = storage.all('State').values()
    states_list = []
    print(all_state)
    if request.method == "GET":
        for state in all_states:
            states_list.append(state.to_dict())
        return jsonify(list_states)



