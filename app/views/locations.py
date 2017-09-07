from flask import jsonify, request,  Response, json

from app import myapp
from app.services.location_services import validate_and_add_location, fetch_all_locations, validate_and_upload_locations, fetch_location_with, delete_location_with
from app.services.location_services import validate_and_add_campus, fetch_all_campus, validate_and_upload_campus, fetch_campus_with, delete_campus_with


@myapp.route('/api/locations', methods = ['GET', 'POST'])
def locations():
    if request.method == 'POST':
        return validate_and_add_location(request.form)
    else:
        return jsonify(success=True, items=fetch_all_locations(is_plain_dict=False, args=request.args))

@myapp.route('/api/locations/<location_id>', methods = ['GET', 'DELETE'])
def locations_with(location_id):
    if request.method == 'DELETE':
        return delete_location_with(id=location_id)
    else:
        return fetch_location_with(id=location_id)

@myapp.route('/api/campus/<campus_id>', methods = ['GET', 'DELETE'])
def campus_with(campus_id):
    if request.method == 'DELETE':
        return delete_campus_with(id=campus_id)
    else:
        return fetch_campus_with(id=campus_id)

@myapp.route('/api/campus', methods = ['GET', 'POST'])
def campus():
    if request.method == 'POST':
        return validate_and_add_campus(request.form)
    else:
        campus = fetch_all_campus()
        return jsonify(success=True, items=campus)


@myapp.route('/api/locations/upload', methods=['POST'])
def upload_locations():
    # datetime.fromtimestamp(your_timestamp / 1e3)
    ustr = request.files['locations'].read()
    reset = request.args.get('reset', False)
    success, count = validate_and_upload_locations(ustr, reset)
    return jsonify(success=success, count=count)

@myapp.route('/api/locations/download', methods=['GET'])
def download_locations():
    resp = fetch_all_locations(is_plain_dict=True)
    return Response(
        str(resp),
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=locations.json"})

@myapp.route('/api/campus/upload', methods=['POST'])
def upload_campus():
    # datetime.fromtimestamp(your_timestamp / 1e3)
    ustr = request.files['campus'].read()
    reset = request.args.get('reset', False)
    status, count = validate_and_upload_campus(ustr, reset)
    return jsonify(success=status, count=count)

@myapp.route('/api/campus/download', methods=['GET'])
def download_campus():
    resp = fetch_all_campus()
    return Response(
        str(resp),
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=campus.json"})
