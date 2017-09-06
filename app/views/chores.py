from flask import jsonify, request,  Response, json
from app import myapp

from app.services.chores_services import validate_and_add_announcement, fetch_all_announcement, delete_event_with, delete_announcement_with
from app.services.chores_services import fetch_all_events, validate_and_add_event, validate_and_add_participants, fetch_all_event_participants
@myapp.route('/api/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        return validate_and_add_announcement(request.form)
    else:
        return fetch_all_announcement()

@myapp.route('/api/announcements/<announcement_id>', methods=['DELETE'])
def announcement_with(announcement_id):
    return delete_announcement_with(id=announcement_id)

@myapp.route('/api/events', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        return validate_and_add_event(request.form)
    else:
        return fetch_all_events(request.args)

@myapp.route('/api/events/<event_id>', methods=['GET', 'POST', 'DELETE'])
def event_participants(event_id):
    if request.method == 'POST':
        count = validate_and_add_participants(event_id, request.form.get('participants', ''))
        return jsonify(success=True, item=count)
    elif request.method == 'DELETE':
        return delete_event_with(id=event_id)
    else:
        return fetch_all_event_participants(event_id=event_id)
