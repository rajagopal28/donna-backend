from flask import jsonify, request,  Response, json
from ast import literal_eval
from app.models.office import User, Campus, Location
from app import myapp

from app.services.user_services import validate_and_add_user, fetch_all_users, validate_input_and_authenticate

@myapp.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        return validate_and_add_user(request.form)
    else:
        return fetch_all_users()

@myapp.route('/api/login', methods=['POST'])
def authenticate_user():
    return validate_input_and_authenticate(request.form)

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
