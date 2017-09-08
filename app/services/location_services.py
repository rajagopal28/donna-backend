from flask import jsonify
from ast import literal_eval

from app import db
from app.models.office import Location, Campus

def validate_and_add_location(form):
    success, new_loc = validate_and_save_location(form, False)
    if success:
        return jsonify(success=True, item=new_loc.to_dict()), 200
    else:
        return jsonify(success=False, message='Missing required fields!'), 400


def fetch_all_locations(is_plain_dict=False, args=None):
    locations = []
    if args and args.get('campusId', None):
        campus_id = args.get('campusId')
        locations = Location.query.filter_by(campus_id=campus_id).all()
    else:
        locations = Location.query.all()
    return [loc.to_plain_dict() if is_plain_dict else loc.to_dict() for loc in locations]


def validate_and_add_campus(form):
    success, new_campus = validate_and_save_campus(form)
    if success:
        return jsonify(success=True, item=new_campus.to_dict()), 200
    else:
        return jsonify(success=False, message='Missing required fields!'), 400

def fetch_all_campus():
    campuses = Campus.query.all()
    return [campus.to_dict() for campus in campuses]

def fetch_location_with(id=None):
    return find_or_delete_location_with(id=id)

def delete_location_with(id=None):
    return find_or_delete_location_with(id=id, should_delete=True)

def delete_location_with(id=None):
    return find_or_delete_location_with(id=id, should_delete=True)

def find_or_delete_location_with(id=None, should_delete=False):
    location = Location.query.filter_by(id=id).first()
    if location:
        if should_delete:
            db.session.delete(location)
            db.session.commit()
        return jsonify(item=location.to_dict(), success=True), 200
    else:
        return jsonify(message='Requested Record Not Available!', success=False), 404

def fetch_campus_with(id=None):
    return find_or_delete_campus_with(id=id)

def delete_campus_with(id=None):
    return find_or_delete_campus_with(id=id, should_delete=True)

def find_or_delete_campus_with(id=None, should_delete=False):
    campus = Campus.query.filter_by(id=id).first()
    if campus:
        if should_delete:
            db.session.delete(campus)
            db.session.commit()
        return jsonify(item=campus.to_dict(), success=True), 200
    else:
        return jsonify(message='Requested Record Not Available!', success=False), 404

def validate_and_upload_locations(ustr, reset):
    locations = literal_eval(ustr.decode().replace("'", '"'))
    if reset :
        Location.query.delete()
        db.session.commit()
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
    floor = form.get('floor', 1)
    if latitude and longitude and name :
        if (not skip_campus) and (not campus):
            return False, None
        else:
            new_loc = Location(name=name, latitude=latitude, longitude=longitude, campus_id=campus, floor=floor)
            new_loc.save()
            return True, new_loc
    return False, None

def validate_and_save_campus(form):
    name = form.get('name', None)
    latitude = form.get('latitude', None)
    longitude = form.get('longitude', None)
    campus_number = form.get('campusNumber', None)
    if name and latitude and longitude:
        new_campus = Campus(name=name, latitude=latitude, longitude=longitude, campus_number=campus_number)
        new_campus.save()
        return True, new_campus
    else:
        return False, None

def validate_and_upload_campus(ustr, reset):
    campus = literal_eval(ustr.decode().replace("'", '"'))
    if reset :
        Campus.query.delete()
        db.session.commit()
    count = 0
    status = False
    for campu in campus:
        status, item = validate_and_save_campus(campu)
        count += (1 if status else 0)
    return status, count
