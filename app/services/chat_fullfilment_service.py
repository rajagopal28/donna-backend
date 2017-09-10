from flask import jsonify
import json
from datetime import datetime, timedelta

from app.models.office import User, Location
from app.models.chores import Event, Announcement, EventParticipant

def process_and_fullfill_chat_request(input_payload):
    # print(input_payload)
    if validate_input_payload(input_payload):
        # print('payload valid')
        input_json =  input_payload['result']
        context = input_json['contexts']
        existing_response = input_json['fulfillment']['speech']
        action = input_json['action']
        resp = {
            'speech': existing_response,
            'displayText': existing_response,
            'source': 'DonnaFulFillmentBackend'
        }
        if validate_payload_parameters(input_json):
            parameters = input_json['parameters']
            print('Parameters Pre...')
            print(parameters)
            # print(resp)
            if action == 'schedule-meeting-request':
                new_response, parameters = process_schedule_meeting(parameters, resp, input_json)
            elif action == 'view-meetings-request':
                new_response, parameters = process_view_meeting_request(parameters, resp, input_json)
            elif action == 'view-person-info-request':
                # this also covers the navigate-to-person-location-request type
                new_response, parameters = process_get_person_info_request(parameters, resp)
            elif action == 'view-person-location-request':
                new_response, parameters = process_get_person_info_request(parameters, resp)
            elif action == 'view-location-info-request':
                new_response, parameters = process_get_location_info_request(parameters, resp)
            elif action == 'route-to-location-request':
                new_response, parameters = process_direction_to_given_location(parameters, resp, input_json)
            elif action == 'view-office-announcements':
                new_response, parameters = process_fetch_office_announcements(parameters, resp)
            resp['speech'] = new_response
            resp['displayText'] = new_response

            resp['data'] = {
            "web" : {
                "parameters" : parameters
            }}
            resp['contextOut'] = context
            resp['parameters'] = parameters
            print('Parameters Post...')
            print(parameters)
        return json.dumps(resp)
    return json.dumps(input_payload)

def validate_payload_parameters(input_payload=None):
    if input_payload:
        parameters = input_payload.get('parameters', None)
        # print(parameters)
        if parameters:
            return True
    return False

def validate_input_payload(input_payload=None):
    if input_payload:
        result = input_payload.get('result', None)
        if result:
            action = result.get('action', None)
            fulfillment = result.get('fulfillment', None)
            if action and fulfillment and fulfillment.get('speech', None):
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
        # print('token='+token)
        print('auth success')
        user = User.query.filter_by(username=token).first()
        # print('found user..'+ user.username)
        if user:
            event_p = EventParticipant.query.filter_by(participant_id=user.id).all()
            events = [ep.event for ep in event_p]
    else:
        events = Event.query.all()
    event_list = ', '.join([(e.title+' From: '+dstr(e.event_start)+' Till: '+dstr(e.event_end)) for e in events])
    return event_list, parameters

def process_direction_to_given_location(parameters, payload, input_json):
    name = parameters.get('campus-location', None)
    authenticated, token = validate_auth_context(input_json)
    if authenticated and name:
        user = User.query.filter_by(username=token).first()
        location = Location.query.filter_by(name=name).first()
        if user and location and user.location:
            speech = 'Taking you to Location: %r with co-ordinates(%r, %r)'%(location.name, str(location.latitude), str(location.longitude))
            if  location.campus and user.location.campus and user.location.campus.id == location.campus.id:
                speech += ' is located at Campus: %r'%(location.campus.name)
            else:
                speech='You are not in the same campus to View Routes!'
                parameters['noRoute'] = 'true'
            parameters['fromLocation'] = user.location.to_dict()
            parameters['toLocation'] = location.to_dict()
            return speech, parameters
        elif not user:
            return 'Invalid User Token!', parameters
        elif not location:
            return 'Not a valid Location', parameters
        else:
            return 'User has no location to route to!', parameters
    return payload['speech'], parameters

def process_get_location_info_request(parameters, payload):
    # bring logic to validate and fetch location info
    name = parameters.get('campus-location', None)
    if name:
        location = Location.query.filter_by(name=name).first()
        if location:
            speech = 'Location: %r with co-ordinates(%r, %r)'%(location.name, str(location.latitude), str(location.longitude))
            if location.campus:
                speech += ' is located at Campus: %r'%(location.campus.name)
                parameters['location'] = location.to_dict()
            return speech, parameters
    return payload['speech'], parameters

def process_fetch_office_announcements(parameters, payload):
    # bring logic to validate and fetch announcements
    e_type = parameters.get('event-type', None)
    response_string = payload['speech']
    announcements = []
    if e_type != 'food':
        # get food related announcements
        announcements = Announcement.query.all()
    else:
        announcements = Announcement.query.filter_by(category=e_type).all()
    if len(announcements) > 0:
        response_string = ", ".join([(a.title+' From: '+dstr(a.valid_from)+' Till: '+dstr(a.valid_till)) for a in announcements])
    return response_string, parameters

def process_get_person_info_request(parameters, payload):
    # fetch info about the given person
    first_name = parameters.get('office-user', None)
    if first_name:
        user = User.query.filter_by(first_name=first_name).first()
        if user:
            speech = 'User: ' + user.first_name + ' ' + user.last_name
            if user.location:
                speech += ' is located at ' + user.location.name
                parameters['location'] = user.location.to_dict()
            return speech, parameters
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
    if location_name == 'your_location':
        location = owner.location
    else:
        location = Location.query.filter_by(name=location_name).first()
    if event_date == 'today':
        now = datetime.today()
        event_date = now.strftime('%Y-%m-%d')
    whole_date = event_date + ' ' + event_time
    start = datetime.strptime(whole_date, '%Y-%m-%d %H:%M:%S')
    end = (start + timedelta(minutes=30))
    if owner and user and location:
        title = owner.first_name + '\'s meeting with ' + user.first_name + ' at ' + location.name
        meeting = Event(title=title, description=title, event_start=start, event_end=end, location_id=location.id)
        meeting.save()
        participants = [owner]
        if owner.id != user.id:
            participants.append(user)
        for p in participants:
            ep = EventParticipant(participant_id=p.id, event_id=meeting.id)
            ep.save()
        return True
    return False

def dstr(date_to_change):
    return date_to_change.strftime('%d, %b %Y - %H:%M') if date_to_change else ''
