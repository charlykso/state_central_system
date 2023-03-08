#!/usr/bin/python3
"""object that handles the user route for the api"""
from models.owner import Owner
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/owners", methods=['GET'],
                 strict_slashes=False)
@app_views.route("/owners/<owner_id>", methods=['GET'],
                 strict_slashes=False)
def get_owners(owner_id=None):
    """
    get all owners
    or get any user with the owner_id that is passed
    """
    new_list = []
    key = "Owner." + str(owner_id)
    if owner_id is None:
        objs = storage.all(Owner)
        for key, value in objs.items():
            new_list.append(value.to_dict())
    elif key in storage.all(Owner).keys():
        return jsonify(storage.all(Owner)[key].to_dict())
    else:
        abort(404)
    return jsonify(new_list)


@app_views.route("/owners/<owner_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_owner(owner_id=None):
    """
    delete any peoperty owner that the owner_id is passed
    """
    owner = storage.get(Owner, owner_id)
    if owner is None:
        abort(404)
    owner.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/owners", methods=['POST'],
                 strict_slashes=False)
def create_owner():
    """
    create a new property owner
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "firstname" not in request.get_json():
        abort(400, "Missing firstname")
    if "lastname" not in request.get_json():
        abort(400, "Missing lastname")
    if "phone_no" not in request.get_json():
        abort(400, "Missing phone number")
    owner = Owner(**request.get_json())
    owner.save()
    return jsonify(owner.to_dict()), 201


@app_views.route("/owners/<owner_id>", methods=['PUT'],
                 strict_slashes=False)
def update_owner(owner_id=None):
    """
    update any property owner the id is passed
    """
    owner = storage.get(Owner, owner_id)
    if owner is None:
        abort(404)
    key = "Owner." + str(owner_id)
    if key not in storage.all(Owner).keys():
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    # if "firstname" not in request.json():
    #     abort(400, "Missing firstname")
    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(owner, key, value)
    owner.save()
    return jsonify(owner.to_dict()), 200
