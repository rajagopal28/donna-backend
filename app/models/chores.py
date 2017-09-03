from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
from app import db

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(50))
    event_start = db.Column(DateTime)
    event_end = db.Column(DateTime)
    description = db.Column(String(50))
    location_id = db.Column(Integer, ForeignKey('locations.id'))
    location = relationship("Location")
    event_participants = relationship("EventParticipant", back_populates="event")

    def __init__(self, title=None, description=None, event_start=None, event_end=None, location_id=None):
        self.title = title
        self.description = description
        self.event_start = event_start
        self.event_end = event_end
        self.location_id = location_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'title': self.title,
            'description': self.description,
            'eventStart': self.event_start.timestamp()*1e3,
            'eventEnd': self.event_end.timestamp()*1e3,
            'locationId': self.location_id,
            'location' : self.location.to_dict() if self.location else None,
            'participants': [ep.to_dict(recurse=False) for ep in self.event_participants]
        }

    def __repr__(self):
        return '<Event %r>' % (self.title)

class EventParticipant(db.Model):
    __tablename__ = 'event_participants'
    id = db.Column(Integer, primary_key=True)
    event_id = db.Column(Integer, ForeignKey('events.id'))
    participant_id = db.Column(Integer, ForeignKey('users.id'))
    event = relationship("Event", back_populates="event_participants")
    participant = relationship("User")

    def __init__(self, event_id=None, participant_id=None):
        self.event_id = event_id
        self.participant_id = participant_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self, recurse=True):
        return {
            'id' : self.id,
            'eventId': self.event_id,
            'participantId': self.participant_id,
            'participant': self.participant.to_dict(),
            'event': self.event.to_dict() if recurse else None
        }

    def __repr__(self):
        return '<EventParticipant %r>' % (self.event.title)



class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(50))
    description = db.Column(String(150))
    category = db.Column(String(50))
    valid_from = db.Column(DateTime)
    valid_till = db.Column(DateTime)
    created_ts = db.Column(DateTime)

    def __init__(self, title=None, description=None, valid_from=None, valid_till=None, category=None):
        self.title = title
        self.description = description
        self.category = category
        self.valid_from = valid_from
        self.valid_till = valid_till
        self.created_ts = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'validFrom': self.valid_from.timestamp()*1e3,
            'validTill' : self.valid_till.timestamp()*1e3,
            'createdTS' : self.created_ts.timestamp()*1e3
        }

    def __repr__(self):
        return '<Announcement %r>' % (self.title)
