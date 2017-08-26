from flask import jsonify, request

from app.models.office import User, Campus, Location
from app import myapp


@myapp.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        fname = request.form.get('firstName', None)
        lname = request.form.get('lastName', None)
        uname = request.form.get('username', None)
        password = request.form.get('password', None)
        location_id = request.form.get('location', None)
        new_user = User(first_name=fname, last_name=lname, username=uname, password=password, location_id=location_id)
        new_user.save()
        return jsonify(success=True, item=new_user.to_dict())
    else:
        users = User.query.all()
        response = [user.to_dict() for user in users]
        return jsonify(items=response, success=True)

@myapp.route('/api/locations', methods = ['GET', 'POST'])
def locations():
    if request.method == 'POST':
        latitude = request.form.get('latitude', None)
        longitude = request.form.get('longitude', None)
        campus = request.form.get('campus', None)
        new_loc = Location(latitude=latitude, longitude=longitude, campus_id=campus)
        new_loc.save()
        return jsonify(success=True, item=new_loc.to_dict())
    else:
        locations = Location.query.all()
        response = [loc.to_dict() for loc in locations]
        return jsonify(items=response, success=True)

@myapp.route('/api/campus', methods = ['GET', 'POST'])
def campus():
    if request.method == 'POST':
        name = request.form.get('name', None)
        latitude = request.form.get('latitude', None)
        longitude = request.form.get('longitude', None)
        new_campus = Campus(name=name, latitude=latitude, longitude=longitude)
        new_campus.save()
        return jsonify(success=True, item=new_campus.to_dict())
    else:
        campuses = Campus.query.all()
        response = [campus.to_dict() for campus in campuses]
        return jsonify(items=response, success=True)


@myapp.route('/api/login', methods=['POST'])
def authenticate_user():
    uname = request.form.get('username', None)
    passwd = request.form.get('password', None)
    user = User.query.filter_by(username=uname, password=passwd).first()
    return jsonify(success=True, item=user.to_dict())
