from flask import jsonify, request,  Response, json
from app import myapp

from app.services.user_services import validate_and_add_user, fetch_all_users, delete_user_with, fetch_user_with
from app.services.user_services import validate_input_and_authenticate, validate_and_upload_users

from app.services.chat_fullfilment_service import process_and_fullfill_chat_request

@myapp.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        return validate_and_add_user(request.form)
    else:
        response = fetch_all_users(is_plain_dict=False, args=request.args)
        return jsonify(items=response, success=True)

@myapp.route('/api/users/<user_id>', methods=['GET', 'DELETE'])
def user_with(user_id):
    if request.method == 'DELETE':
        return delete_user_with(id=user_id)
    else:
        return fetch_user_with(id=user_id)


@myapp.route('/api/users/login', methods=['POST'])
def authenticate_user():
    return validate_input_and_authenticate(request.form)

@myapp.route('/api/users/upload', methods=['POST'])
def upload_users():
    # datetime.fromtimestamp(your_timestamp / 1e3)
    ustr = request.files['users'].read()
    reset = request.args.get('reset', False)
    status, count = validate_and_upload_users(ustr, reset)
    return jsonify(success=status, count=count)

@myapp.route('/api/users/download', methods=['GET'])
def download_users():
    resp = fetch_all_users(is_plain_dict=True, args=request.args)
    return Response(
        str(resp),
        mimetype="application/json",
        headers={"Content-disposition":
                 "attachment; filename=users.json"})

@myapp.route('/api/ai/fulfillment', methods=['POST'])
def fullfill_chat_request():
    return process_and_fullfill_chat_request(request.json)
