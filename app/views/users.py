from flask import jsonify, request,  Response, json
from ast import literal_eval
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

@myapp.route('/api/users/upload', methods=['POST'])
def upload_users():
    # datetime.fromtimestamp(your_timestamp / 1e3)
    ustr = request.files['users'].read()
    users = literal_eval(ustr.decode().replace("'", '"'))
    if request.args.get('reset', False) :
        User.query.delete()
    for user in users:
        first_name = user["firstName"]
        last_name = user["lastName"]
        username = user["username"]
        password = user["password"]
        location_id =  user["locationId"]  if "locationId" in user else None
        new_user = User(first_name=first_name, last_name=last_name, username=username, password=password, location_id=location_id)
        new_user.save()
        # print(new_user)
    return jsonify(success=True, count=len(users))

@myapp.route('/api/users/download', methods=['GET'])
def download_users():
    users = User.query.all()
    resp = [user.to_plain_dict() for user in users]
    return Response(
        str(resp),
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=users.json"})

@myapp.route('/api/locations/upload', methods=['POST'])
def upload_locatuons():
    # datetime.fromtimestamp(your_timestamp / 1e3)
    ustr = request.files['locations'].read()
    locations = literal_eval(ustr.decode().replace("'", '"'))
    if request.args.get('reset', False) :
        Location.query.delete()
    for location in locations:
        name = location["name"]
        latitude = location["latitude"]
        longitude = location["longitude"]
        campus_id =  location["campusId"]  if "campusId" in location else None
        new_loc = Location(name=name, latitude=latitude, longitude=longitude, campus_id=campus_id)
        new_loc.save()
        # print(new_loc)
    return jsonify(success=True, count=len(locations))

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
    campus = literal_eval(ustr.decode().replace("'", '"'))
    if request.args.get('reset', False) :
        Campus.query.delete()
    for campu in campus:
        name = campu["name"]
        longitude = campu["longitude"]
        latitude = campu["latitude"]
        new_campu = Campus(name=name, latitude=latitude, longitude=longitude)
        new_campu.save()
        # print(new_campu)
    return jsonify(success=True, count=len(campus))

@myapp.route('/api/campus/download', methods=['GET'])
def download_campus():
    campus = Campus.query.all()
    resp = [campu.to_dict() for campu in campus]
    return Response(
        str(resp),
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=campus.json"})
