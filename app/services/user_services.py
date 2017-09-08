from flask import jsonify
from ast import literal_eval

from app import db
from app.models.office import User, Location

def validate_and_add_user(form):
    status, new_user = validate_and_save_user(form, skip_location=False)
    if status:
        return jsonify(success=True, item=new_user.to_dict())
    else:
        return jsonify(success=False, message='Missing required fields!'), 400

def fetch_all_users(is_plain_dict=False, args=None):
    if args :
        campus_id = args.get('campusId', None)
        if campus_id:
            locations = Location.query.filter_by(campus_id=campus_id).all()
            users = User.query.filter(User.location_id.in_([l.id for l in locations])).all()
    else:
        users = User.query.all()
    return [user.to_plain_dict() if is_plain_dict else user.to_dict() for user in users]

def fetch_user_with(id=None):
    return find_or_delete_user_with(id=id)

def find_or_delete_user_with(id=None, should_delete=False):
    user = User.query.filter_by(id=id).first()
    if user:
        if should_delete:
            db.session.delete(user)
            db.session.commit()
        return jsonify(item=user.to_dict(), success=True), 200
    else:
        return jsonify(message='Requested Record Not Available!', success=False), 404

def delete_user_with(id=None):
    return find_or_delete_user_with(id=id, should_delete=True)

def validate_input_and_authenticate(form):
    uname = form.get('username', None)
    passwd = form.get('password', None)
    if uname and passwd:
        user = User.query.filter_by(username=uname, password=passwd).first()
        if user:
            return jsonify(success=True, item=user.to_dict())
        else:
            return jsonify(success=False, message='Authentication Failed!'), 403
    else:
        return jsonify(success=False, message='Missing required fields!'), 401

def validate_and_upload_users(ustr, reset):
    users = literal_eval(ustr.decode().replace("'", '"'))
    if reset :
        User.query.delete()
        db.session.commit()
    count = 0
    status = False
    for user in users:
        status, u = validate_and_save_user(user, True)
        count += 1 if status else 0
        # print(new_user)
    return status, count
def validate_and_save_user(form, skip_location):
    first_name = form.get("firstName", None)
    last_name = form.get("lastName", None)
    username = form.get("username", None)
    password = form.get("password", None)
    location_id = form.get("locationId", None)  if "locationId" in form else None
    if first_name and last_name and username and password:
        if (not skip_location) and (not location_id):
            return False, None
        new_user = User(first_name=first_name, last_name=last_name, username=username, password=password, location_id=location_id)
        new_user.save()
        return True, new_user
    return False, None
