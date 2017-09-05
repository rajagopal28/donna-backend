from flask import jsonify
import json
from datetime import datetime, timedelta

from app.models.office import User, Location
from app.models.chores import Event, Announcement, EventParticipant

def process_and_fullfill_chat_request(input_payload):
    print(input_payload)
    if validate_input_payload(input_payload):
        print('payload valid')
        input_json =  input_payload['result']
        action = input_json['action']
        parameters = input_json['parameters']
        context = input_json['contexts']
        existing_response = input_json['fulfillment']['speech']
        resp = {
            'speech': existing_response,
            'displayText': existing_response,
            'data': parameters,
            'contextOut': context,
            'source': 'DonnaFulFillmentBackend'
        }
        print(resp)
        if action == 'schedule-meeting-request':
            new_response, parameters = process_schedule_meeting(parameters, resp, input_json)
        elif action == 'view-meetings-request':
            new_response, parameters = process_view_meeting_request(parameters, resp, input_json)
        elif action == 'view-person-info-request':
            new_response, parameters = process_get_person_info_request(parameters, resp)
        elif action == 'view-person-location-request':
            new_response, parameters = process_get_person_info_request(parameters, resp)
        elif action == 'route-to-location-request':
            new_response, parameters = process_direction_to_given_location(parameters, resp)
        elif action == 'route-to-person-location-request':
            new_response, parameters = process_direction_to_given_person_location(parameters, resp)
        elif action == 'view-office-announcements':
            new_response, parameters = process_fetch_office_announcements(parameters, resp)
        resp['speech'] = new_response
        resp['displayText'] = new_response
        return json.dumps(resp)
    return json.dumps(input_payload)

def validate_input_payload(input_payload=None):
    if input_payload:
        result = input_payload.get('result', None)
        if result:
            fulfillment = result.get('fulfillment', None)
            parameters = result.get('parameters', None)
            if fulfillment and fulfillment.get('speech', None) and parameters:
                return True
    return False

def validate_auth_context(result=None):
    if result:
        contexts = result.get('contexts', None)
        if contexts and len(contexts) > 0:
            auth_context = [c for c in contexts if c.get('name', None) =='auth'][0]
            # print(auth_context)
            if auth_context :
                auth_params = auth_context.get('parameters',None)
                if auth_params and auth_params.get('token', None):
                    return True, auth_params.get('token')
    return False, None

def process_view_meeting_request(parameters, payload, input_json):
    # bring logic to validate and fetch all user events
    authenticated, token = validate_auth_context(input_json)
    events = []
    if authenticated:
        print('token='+token)
        print('auth success')
        user = User.query.filter_by(username=token).first()
        print('found user..'+ user.username)
        if user:
            event_p = EventParticipant.query.filter_by(participant_id=user.id).all()
            events = [ep.event for ep in event_p]
    else:
        events = Event.query.all()
    event_list = ', '.join([e.title for e in events])
    return event_list, parameters

def process_direction_to_given_location(parameters, payload):
    # bring logic to validate and fetch location info
    return payload['speech'], parameters

def process_direction_to_given_person_location(parameters, payload):
    # bring logic to validate and fetch location info
    return payload['speech'], parameters

def process_fetch_office_announcements(parameters, payload):
    # bring logic to validate and fetch announcements
    return payload['speech'], parameters

def process_get_person_info_request(parameters, payload):
    # fetch info about the given person
    return payload['speech'], parameters

def process_schedule_meeting(parameters, payload, input_json):
    resp_string = payload['speech']
    # validate parameters
    s_date = parameters.get('date', None)
    participant_name = parameters.get('office-user', None)
    location_name = parameters.get('campus-location', None)
    s_time = parameters.get('time', None)

    if s_date and participant_name and location_name and s_time:
        # validate auth
        authenticated, token = validate_auth_context(input_json)
        if authenticated:
            # process event add here
            status = validate_input_fetch_data_and_add_event(event_date=s_date, participant_name=participant_name, location_name=location_name, event_time=s_time, creator=token)
            # bring logic to validate and add meeting event
            resp_string = ('Added!' + resp_string) if status else 'Not Added Event!!'
        else:
            resp_string = 'Not authenticated to Add Event!!'
    else:
        resp_string = 'Oops!! Missing required meeting info. Please try again'
    return resp_string, parameters

def validate_input_fetch_data_and_add_event(event_date, participant_name, location_name, event_time, creator):
    owner = User.query.filter_by(username=creator).first()
    user = User.query.filter_by(first_name=participant_name).first()
    location = Location.query.filter_by(name=location_name).first()
    whole_date = event_date + ' ' + event_time
    start = datetime.strptime(whole_date, '%Y-%m-%d %H:%M:%S')
    end = (start + timedelta(minutes=30))
    if owner and user and location:
        title = owner.first_name + '\'s meeting with ' + user.first_name + ' at ' + location.name
        meeting = Event(title=title, description=title, event_start=start, event_end=end, location_id=location.id)
        meeting.save()
        return True
    return False
