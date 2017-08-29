from flask import jsonify
from ast import literal_eval

from app.models.office import Location, Campus

def validate_and_add_location(form):
    success, new_loc = validate_and_save_location(form, False)
    if success:
        return jsonify(success=True, item=new_loc.to_dict())
    else:
        return jsonify(success=False, message='Missing required fields!')


def fetch_all_locations():
    locations = Location.query.all()
    response = [loc.to_dict() for loc in locations]
    return response


def validate_and_add_campus(form):
    success, new_campus = validate_and_save_campus(form)
    if success:
        return jsonify(success=True, item=new_campus.to_dict())
    else:
        return jsonify(success=False, message='Missing required fields!')

def fetch_all_campus():
    campuses = Campus.query.all()
    response = [campus.to_dict() for campus in campuses]
    return jsonify(items=response, success=True)

def validate_and_upload_locations(ustr, reset):
    locations = literal_eval(ustr.decode().replace("'", '"'))
    if reset :
        Location.query.delete()
    count = 0
    status = False
    for location in locations:
        status, loc = validate_and_save_location(location, True)
        count = count + (1 if status else 0)
        # print(new_loc)
    return status, count

def validate_and_save_location(form, skip_campus):
    latitude = form.get('latitude', None)
    longitude = form.get('longitude', None)
    name = form.get('name', None)
    campus = form.get('campusId', None)
    if latitude and longitude and name :
        if not skip_campus and not campus:
            return False, None
        else:
            new_loc = Location(name=name, latitude=latitude, longitude=longitude, campus_id=campus)
            new_loc.save()
            return True, new_loc
    return False, None

def validate_and_save_campus(form):
    name = form.get('name', None)
    latitude = form.get('latitude', None)
    longitude = form.get('longitude', None)
    if name and latitude and longitude:
        new_campus = Campus(name=name, latitude=latitude, longitude=longitude)
        new_campus.save()
        return True, new_campus
    else:
        return False, None

def validate_and_upload_campus(ustr, reset):
    campus = literal_eval(ustr.decode().replace("'", '"'))
    if reset :
        Campus.query.delete()
    count = 0
    status = False
    for campu in campus:
        status, item = validate_and_save_campus(campu)
        count += (1 if status else 0)
    return status, count
