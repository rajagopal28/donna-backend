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
        dict_val = self.to_plain_dict()
        if 'password' in dict_val: del dict_val['password']
        dict_val["location"] = self.location.to_dict() if self.location else None
        dict_val["createdTS"] = self.created_ts.timestamp()*1e3
        dict_val["lastupdatedTS"] = self.lastupdated_ts.timestamp()*1e3
        return dict_val

    def to_plain_dict(self):
         return {
            'id' : self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'username': self.username,
            'password' : self.password,
            'locationId': self.location_id if self.location_id else 0
        }

    def __repr__(self):
        return '<User %r>' % (self.username)



class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(Integer, primary_key=True)
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    name = db.Column(String(50))
    floor = db.Column(Integer)
    campus_id = Column(Integer, ForeignKey('campus.id'))
    campus = relationship("Campus", back_populates="locations")

    def __init__(self, latitude=None, longitude=None, name=None, campus_id=None, floor=None):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.campus_id = campus_id
        self.floor = floor

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        dict_val = self.to_plain_dict()
        dict_val['campus'] =self.campus.to_dict() if self.campus else None
        return dict_val

    def to_plain_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'campusId': self.campus_id,
            'floor' : self.floor
        }
    def __repr__(self):
        return '<Location %r>' % (self.name)


class Campus(db.Model):
    __tablename__ = 'campus'
    id = db.Column(Integer, primary_key=True)
    latitude = db.Column(Float)
    longitude = db.Column(Float)
    name = db.Column(String(50))
    campus_number =  db.Column(Integer)
    locations = relationship("Location", back_populates="campus")

    def __init__(self, latitude=None, longitude=None, name=None, campus_number=None):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.campus_number = campus_number

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'campusNumber' : self.campus_number
        }

    def __repr__(self):
        return '<Campus %r>' % (self.name)
