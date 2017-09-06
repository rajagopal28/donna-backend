from flask import jsonify
import datetime

from app import db
from app.models.office import User
from app.models.chores import Announcement, Event, EventParticipant

def validate_and_add_announcement(form):
    now = datetime.datetime.now()
    title = form.get("title", None)
    description = form.get("description", None)
    e_start = form.get("validFrom", None)
    e_end = form.get("validTill", None)
    category = form.get("category", None)
    # datetime.fromtimestamp(your_timestamp / 1e3)
    if title and description and category and e_start and e_end:
        start = datetime.datetime.fromtimestamp(float(e_start)/1e3)
        end = datetime.datetime.fromtimestamp(float(e_end)/1e3)
        ancmt = Announcement(title=title, description=description, category=category, valid_from=start, valid_till=end)
        ancmt.save()
        return jsonify(success=True, item=ancmt.to_dict()), 200
    else:
        return jsonify(success=False, message="Missing Fields!!!"), 401

def fetch_all_announcement():
    announcements = Announcement.query.all()
    response = [a.to_dict() for a in announcements]
    return jsonify(items=response, success=True)


def validate_and_add_event(form):
    now = datetime.datetime.now()
    title = form.get("title", None)
    description = form.get("description", None)
    e_start = form.get("eventStart", None)
    e_end = form.get("eventEnd", None)
    participant_ids = form.get("participantIds", '')
    location_id = form.get('locationId', None)
    # datetime.fromtimestamp(your_timestamp / 1e3)
    if title and description and location_id and e_start and e_end:
        start = datetime.datetime.fromtimestamp(float(e_start)/1e3)
        end = datetime.datetime.fromtimestamp(float(e_end)/1e3)
        event = Event(title=title, description=description, event_start=start, event_end=end, location_id=location_id)
        event.save()
        validate_and_add_participants(event.id, participant_ids)
        return jsonify(success=True, item=event.to_dict()), 200
    else:
        return jsonify(success=False, message="Missing Fields!!!"), 401

def fetch_all_events(args):
    user_id = args.get('userId', None)
    events = []
    if user_id:
        eps = EventParticipant.query.filter_by(participant_id=user_id).all()
        events = [ep.event for ep in eps]
    else:
        events = Event.query.all()
    response = [evt.to_dict() for evt in events]
    return jsonify(items=response, success=True)

def validate_and_add_participants(event_id, participant_ids):
    participants = participant_ids.split(',')
    count = 0
    if len(participants) > 0:
        count = validate_and_add_parsed_participants(event_id=event_id, participants=participants)
        # print(count)
    return count

def validate_and_add_parsed_participants(event_id, participants):
    participant_users = User.query.filter(User.id.in_(participants)).all()
    # print (len(participant_users))
    for p_us in participant_users:
        event_part = EventParticipant(event_id=event_id, participant_id=p_us.id)
        event_part.save()
    return len(participant_users)

def fetch_all_event_participants(event_id):
    participants = EventParticipant.query.filter_by(event_id=event_id).all()
    resp = [p.participant.to_dict() for p in participants]
    return jsonify(success=True, items=resp), 200

def delete_event_with(id=None):
    event = Event.query.filter_by(id=id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify(success=True, item=event.to_dict()), 200
    else:
        return jsonify(message='Requested Record Not Available!', success=False), 404

def delete_announcement_with(id=None):
    announcement = Announcement.query.filter_by(id=id).first()
    if announcement:
        db.session.delete(announcement)
        db.session.commit()
        return jsonify(success=True, item=announcement.to_dict()), 200
    else:
        return jsonify(message='Requested Record Not Available!', success=False), 404
