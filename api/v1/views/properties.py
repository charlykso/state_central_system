#!/usr/bin/python3
"""Objects for properties """

from models.owner import Owner
from models.property import Property
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request
import shortuuid
from api.v1.views.collectives.search_properties import SearchP


@app_views.route("/owners/<owner_id>/properties", methods=['GET'],
                 strict_slashes=False)
def get_properties_for_an_owner(owner_id=None):
    """
    get all properties that is associated to a property owner
    """
    owner = storage.get(Owner, owner_id)
    if owner is None:
        abort(404)
    new_list = []
    for property in owner.properties:
        new_list.append(property.to_dict())
    return jsonify(new_list)


@app_views.route("/properties/<property_id>", methods=['GET'],
                 strict_slashes=False)
@app_views.route('/properties', methods=['GET'],
                 strict_slashes=False)
def get_property(property_id=None):
    """
    retrieve one or all properties
    """
    print(property_id)
    new_list = []
    key = "Property." + str(property_id)
    if property_id is None:
        objs = storage.all(Property)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(Property).keys():
        return jsonify(storage.all(Property)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/property/<unique_id>", methods=['GET'],
                 strict_slashes=False)
def get_property_by_unique_id(unique_id):
    """
    retrieve one properties
    by passing the unique id
    """
    print("God is good")
    print(unique_id)
    new_list = []
    if unique_id is None:
        abort(400, "Missing unique id")
    else:
        result = SearchP.get(Property, unique_id)
        if result is None:
            abort(400, "nothing found")
        print(result)
        return jsonify(result)


@app_views.route("/properties/<property_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_property(property_id=None):
    """
    delete a property that the id was passed
    """
    property = storage.get(Property, property_id)
    if property is None:
        abort(404)
    property.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/owners/<owner_id>/properties", methods=['POST'],
                 strict_slashes=False)
def create_property(owner_id=None):
    """
    create a property for a by it's owner
    by using the user_id to select the user
    """
    if storage.get(Owner, owner_id) is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if storage.get(Owner, request.get_json()["owner_id"]) is None:
        abort(404)
    if "location" not in request.get_json():
        abort(400, "Missing location")
    if "description" not in request.get_json():
        abort(400, "Missing description")
    if "type" not in request.get_json():
        abort(400, "Missing type")

    property = Property(**request.get_json())
    property.owner_id = owner_id
    property.unique_id = str(shortuuid.ShortUUID().random(length=19))
    property.save()

    return jsonify(property.to_dict()), 201


@app_views.route("/property/<property_id>", methods=['PUT'],
                 strict_slashes=False)
def update_property(property_id=None):
    """
    update a property
    by passing the property_id
    """
    key = "Property." + str(property_id)
    if key not in storage.all(Property).keys():
        abort(404)
    property = storage.get(Property, property_id)
    if property is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at",
                       "owner_id", "unique_id"]:
            setattr(property, key, value)
    property.save()
    return jsonify(property.to_dict()), 200
