#!/usr/bin/python3
"""
for checking the status of the api
and stats of the models
"""

from api.v1.views import app_views
from models import storage
from models.property import Property
from models.owner import Owner
from flask import jsonify
from models.base_model import BaseModel, Base


classes = {
	"properties": Property,
	"owners": Owner,
}


@app_views.route("/status", methods=['GET'],
                 strict_slashes=False)
def status():
    """get the api status"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=['GET'],
                 strict_slashes=False)
def stats():
    """get the stats of the models"""
    obj_count = {}
    for key, value in classes.items():
        obj_count[key] = storage.count(value)
    return jsonify(obj_count)


if __name__ == '__main__':
    pass
