from flask import jsonify

from app.models.office import User

def validate_and_add_user(form):
    fname = form.get('firstName', None)
    lname = form.get('lastName', None)
    uname = form.get('username', None)
    password =  form.get('password', None)
    location_id =  form.get('location', None)
    if fname and lname and uname and password and location_id:
        new_user = User(first_name=fname, last_name=lname, username=uname, password=password, location_id=location_id)
        new_user.save()
        return jsonify(success=True, item=new_user.to_dict())
    else:
        return jsonify(success=False, message='Missing required fields!')

def fetch_all_users():
    users = User.query.all()
    response = [user.to_dict() for user in users]
    return jsonify(items=response, success=True)

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
