from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(50))
    last_name = db.Column(String(50))
    username = db.Column(String(50))
    password = db.Column(String(50))
    created_ts = db.Column(DateTime)
    lastupdated_ts = db.Column(DateTime)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship("Location")

    def __init__(self, first_name=None, last_name=None, username=None, password=None, location_id = None):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.location_id = location_id
        self.created_ts = datetime.datetime.now()
        self.lastupdated_ts = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'location' : self.location.to_dict(),
            'created_ts': self.created_ts,
            'lastupdated_ts': self.lastupdated_ts
        }

    def __repr__(self):
        return '<User %r>' % (self.username)



class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(Integer, primary_key=True)
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    campus_id = Column(Integer, ForeignKey('campus.id'))
    campus = relationship("Campus", back_populates="locations")

    def __init__(self, latitude=None, longitude=None, campus_id=None):
        self.latitude = latitude
        self.longitude = longitude
        self.campus_id = campus_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'campus_id': self.campus_id,
            'campus' : self.campus.to_dict()
        }

    def __repr__(self):
        return '<Location %r, %r>' % (self.latitude, self.longitude)


class Campus(db.Model):
    __tablename__ = 'campus'
    id = db.Column(Integer, primary_key=True)
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    name = db.Column(String(50))
    locations = relationship("Location", back_populates="campus")

    def __init__(self, latitude=None, longitude=None, name=None):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }

    def __repr__(self):
        return '<Campus %r>' % (self.name)
