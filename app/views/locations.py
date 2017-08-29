from flask import jsonify, request,  Response, json
from ast import literal_eval

from app.models.office import User, Campus, Location
from app import myapp
from app.services.location_services import validate_and_add_location, fetch_all_locations, validate_and_add_campus, fetch_all_campus, validate_and_upload_locations, validate_and_upload_campus

@myapp.route('/api/locations', methods = ['GET', 'POST'])
def locations():
    if request.method == 'POST':
        return validate_and_add_location(request.form)
    else:
        return jsonify(success=True, items=fetch_all_locations())

@myapp.route('/api/campus', methods = ['GET', 'POST'])
def campus():
    if request.method == 'POST':
        return validate_and_add_campus(request.form)
    else:
        return fetch_all_campus()


@myapp.route('/api/locations/upload', methods=['POST'])
def upload_locations():
    # datetime.fromtimestamp(your_timestamp / 1e3)
    ustr = request.files['locations'].read()
    reset = request.args.get('reset', False)
    success, count = validate_and_upload_locations(ustr, reset)
    return jsonify(success=success, count=count)

@myapp.route('/api/locations/download', methods=['GET'])
def download_locations():
    locations = Location.query.all()
    resp = [location.to_plain_dict() for location in locations]
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
    campus = Campus.query.all()
    resp = [campu.to_dict() for campu in campus]
    return Response(
        str(resp),
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=campus.json"})
