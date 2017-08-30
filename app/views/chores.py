from flask import jsonify, request,  Response, json
from app import myapp

from app.services.chores_services import validate_and_add_announcement, fetch_all_announcement, fetch_all_events, validate_and_add_event, validate_and_add_participants, fetch_all_event_participants
@myapp.route('/api/announcements', methods=['GET', 'POST'])
def announcements():
    if request.method == 'POST':
        return validate_and_add_announcement(request.form)
    else:
        return fetch_all_announcement()

@myapp.route('/api/events', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        return validate_and_add_event(request.form)
    else:
        return fetch_all_events()

@myapp.route('/api/events/<event_id>', methods=['GET', 'POST'])
def event_participants(event_id):
    if request.method == 'POST':
        count = validate_and_add_participants(event_id, request.form.get('participants', ''))
        return jsonify(success=True, item=count)
    else:
        return fetch_all_event_participants(event_id=event_id)
