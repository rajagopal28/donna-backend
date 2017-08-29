from flask import jsonify, request,  Response, json
from app import myapp

from app.services.chores_services import validate_and_add_announcement, fetch_all_announcement

@myapp.route('/api/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        status, ancmt = validate_and_add_announcement(request.form)
        if status:
            return jsonify(success=True, item=ancmt.to_dict())
        else:
            return jsonify(success=False, message="Missing Fields!!!")
    else:
        response = fetch_all_announcement()
        return jsonify(items=response, success=True)
