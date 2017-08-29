from flask import jsonify
from ast import literal_eval

from app.models.office import User

def validate_and_add_user(form):
    status, new_user = validate_and_save_user(form, skip_location=False)
    if status:
        return jsonify(success=True, item=new_user.to_dict())
    else:
        return jsonify(success=False, message='Missing required fields!')

def fetch_all_users(is_plain_dict):
    users = User.query.all()
    return [user.to_plain_dict() if is_plain_dict else user.to_dict() for user in users]

def validate_input_and_authenticate(form):
    uname = request.form.get('username', None)
    passwd = request.form.get('password', None)
    if uname and passwd:
        user = User.query.filter_by(username=uname, password=passwd).first()
        if user:
            return jsonify(success=True, item=user.to_dict())
        else:
            return jsonify(success=False, message='Authentication Failed!')
    else:
        return jsonify(success=False, message='Missing required fields!')

def validate_and_upload_users(ustr, reset):
    users = literal_eval(ustr.decode().replace("'", '"'))
    if reset :
        User.query.delete()
    count = 0
    status = False
    for user in users:
        status, u = validate_and_save_user(user, True)
        count += 1 if status else 0
        # print(new_user)
    return status, count
def validate_and_save_user(form, skip_location):
    first_name = form["firstName"]
    last_name = form["lastName"]
    username = form["username"]
    password = form["password"]
    location_id =  form["locationId"]  if "locationId" in form else None
    if first_name and last_name and username and password:
        if (not skip_location) and (not location_id):
            return False, None
        new_user = User(first_name=first_name, last_name=last_name, username=username, password=password, location_id=location_id)
        new_user.save()
        return True, new_user
    return False, None
