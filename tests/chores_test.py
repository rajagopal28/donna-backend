import json
from tests.base_test import BaseTest
import unittest
from app.models.office import User, Location
from app.models.chores import Announcement, Event, EventParticipant
import time
from io import BytesIO
from datetime import datetime, timedelta

class ChoresManagerTests(BaseTest):

    def test_all_announcements_for_response_with_inserted_data(self):
        now = datetime.now()
        later = now + timedelta(minutes=30)
        a1 = Announcement(title='Announcement1', description='Some desc 1', category='food', valid_from=now, valid_till=later)
        a2 = Announcement(title='Announcement2', description='Some desc 2', category='emergency', valid_from=now, valid_till=later)

        self.test_db.session.add(a1)
        self.test_db.session.add(a2)
        self.test_db.session.commit()

        result = self.app.get('/api/announcements')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 2)
        self.assertEqual(dict_val["items"][0]["title"], a1.title)
        self.assertEqual(dict_val["items"][1]["validFrom"], a1.valid_from.timestamp()*1e3)
        self.assertEqual(dict_val["items"][1]["title"], a2.title)
        self.assertEqual(dict_val["items"][1]["validTill"], a2.valid_till.timestamp()*1e3)
        self.assertEqual(dict_val["success"], True)

    def test_add_announcement_with_valid_data(self):
        now = datetime.now()
        later = (now + timedelta(hours=2))
        data = {
        'title' : 'Announcement3',
        'description' : 'Some announcements 3',
        'category' : 'food',
        'validFrom' : now.timestamp()*1e3,
        'validTill' : later.timestamp()*1e3
        }
        result = self.app.post('/api/announcements',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["title"], data['title'])
        self.assertEqual(dict_val["item"]["validFrom"], data['validFrom'])
        self.assertEqual(dict_val["success"], True)
        announcements = Announcement.query.all()
        self.assertEqual(len(announcements), 1)
        self.assertEqual(announcements[0].valid_till, later)
        self.assertEqual(announcements[0].description, data['description'])

    def test_should_not_add_announcement_with_invalid_data(self):
        now = datetime.now()
        later = (now + timedelta(hours=2))
        data = {
        'title' : 'Announcement3',
        'description' : 'Some announcements 3',
        'category' : 'food',
        'validTill' : later.timestamp()*1e3
        }
        result = self.app.post('/api/announcements',data=data)
        self.assertEqual(result.status_code, 401)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], "Missing Fields!!!")
        self.assertEqual(dict_val["success"], False)
        announcements = Announcement.query.all()
        self.assertEqual(len(announcements), 0)


    def test_all_events_for_given_user_response_with_inserted_data(self):
        now = datetime.now()
        e1 = Event(title='Event 1', description='Some desc 1', event_start=now, event_end=now)
        e2 = Event(title='Event 2', description='Some desc 2', event_start=now, event_end=now)
        u1 = User(first_name='user1', last_name='last1', username='uname1', password='password1')

        self.test_db.session.add(e1)
        self.test_db.session.add(e2)
        self.test_db.session.add(u1)
        self.test_db.session.commit()

        e1_id = e1.id
        u1_id = u1.id
        ep1 = EventParticipant(event_id=e1_id, participant_id=u1.id)
        self.test_db.session.add(ep1)
        self.test_db.session.commit()

        result = self.app.get('/api/events?userId='+str(u1_id))
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 1)
        self.assertEqual(dict_val["items"][0]["title"], e1.title)
        self.assertEqual(dict_val["success"], True)


    def test_delete_announcement_with_given_id(self):
        now = datetime.now()
        a1 = Announcement(title='Announcement1', description='Some desc 1', category='food', valid_from=now, valid_till=now)
        self.test_db.session.add(a1)
        self.test_db.session.commit()

        a1_id = a1.id
        result = self.app.delete('/api/announcements/'+str(a1_id))
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val["item"]["title"], a1.title)
        self.assertEqual(dict_val["success"], True)
        es = Event.query.all()
        self.assertEqual(len(es), 0)

    def test_not_delete_announcement_with_invalid_id(self):
        result = self.app.delete('/api/announcements/13')
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(dict_val['message'], 'Requested Record Not Available!')

    def test_delete_event_with_given_id(self):
        now = datetime.now()
        e1 = Event(title='Event 1', description='Some desc 1', event_start=now, event_end=now)
        self.test_db.session.add(e1)
        self.test_db.session.commit()

        e1_id = e1.id
        result = self.app.delete('/api/events/'+str(e1_id))
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val["item"]["title"], e1.title)
        self.assertEqual(dict_val["success"], True)
        es = Event.query.all()
        self.assertEqual(len(es), 0)

    def test_not_delete_event_with_invalid_id(self):
        result = self.app.delete('/api/events/13')
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(dict_val['message'], 'Requested Record Not Available!')

    def test_all_events_for_response_with_inserted_data(self):
        now = datetime.now()
        e1 = Event(title='Event 1', description='Some desc 1', event_start=now, event_end=now)
        e2 = Event(title='Event 2', description='Some desc 2', event_start=now, event_end=now)

        self.test_db.session.add(e1)
        self.test_db.session.add(e2)
        self.test_db.session.commit()

        result = self.app.get('/api/events')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 2)
        self.assertEqual(dict_val["items"][0]["title"], e1.title)
        self.assertEqual(dict_val["items"][1]["title"], e2.title)
        self.assertEqual(dict_val["success"], True)

    def test_should_not_add_event_with_invalid_data(self):
        now = datetime.now()
        later = (now + timedelta(hours=2))
        data = {
            'title' : 'Event 5',
            'description' : 'Some event 5',
            'eventStart' : now.timestamp()*1e3,
            'eventEnd' : later.timestamp()*1e3,
        }
        result = self.app.post('/api/events',data=data)
        self.assertEqual(result.status_code, 401)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], "Missing Fields!!!")
        self.assertEqual(dict_val["success"], False)
        events = Event.query.all()
        self.assertEqual(len(events), 0)

    def test_add_event_with_valid_data_with_location_without_participants(self):
        l1 = Location(name='loc2',latitude=62.64654, longitude=63.54465, campus_id = 0)
        self.test_db.session.add(l1)
        self.test_db.session.commit()
        l_id = l1.id
        now = datetime.now()
        later = (now + timedelta(hours=1))
        data = {
            'title' : 'Event 5',
            'description' : 'Some event 5',
            'eventStart' : now.timestamp()*1e3,
            'eventEnd' : later.timestamp()*1e3,
            'locationId': l_id
        }
        result = self.app.post('/api/events',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["title"], data['title'])
        self.assertEqual(dict_val["item"]["eventStart"], data['eventStart'])
        self.assertEqual(dict_val["item"]["location"]["name"], l1.name)
        self.assertEqual(dict_val["success"], True)
        events = Event.query.all()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_start, now)
        self.assertEqual(events[0].description, data['description'])
        self.assertEqual(events[0].event_end, later)

    def test_add_event_with_valid_data_with_location_partially_valid_participants(self):
        u1 = User(first_name='User1', last_name='Last3', username='uname13', password='sdfsdf')
        l1 = Location(name='loc2',latitude=62.64654, longitude=63.54465, campus_id = 0)
        self.test_db.session.add(u1)
        self.test_db.session.add(l1)
        self.test_db.session.commit()
        u_id = u1.id
        l_id = l1.id
        now = datetime.now()
        later = (now + timedelta(hours=1))
        data = {
            'title' : 'Event 5',
            'description' : 'Some event 5',
            'eventStart' : now.timestamp()*1e3,
            'eventEnd' : later.timestamp()*1e3,
            'participantIds' : '%r,%r'%(u_id, 3),
            'locationId' : l_id
        }
        result = self.app.post('/api/events',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["title"], data['title'])
        self.assertEqual(dict_val["item"]["eventStart"], data['eventStart'])
        self.assertEqual(dict_val["item"]["location"]["latitude"], l1.latitude)
        self.assertEqual(dict_val["success"], True)
        events = Event.query.all()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_start, now)
        self.assertEqual(events[0].description, data['description'])
        self.assertEqual(events[0].event_end, later)

        event_participants = EventParticipant.query.filter_by(event_id=events[0].id).all()
        self.assertEqual(len(event_participants), 1)
        self.assertEqual(event_participants[0].participant_id, u_id)

    def test_add_event_participants_for_response_with_inserted_data(self):
        now = datetime.now()
        e1 = Event(title='Event 1', description='Some desc 1', event_start=now, event_end=now)
        u1 = User(first_name='User1', last_name='Last3', username='uname131', password='sdfsdf')

        self.test_db.session.add(e1)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        e_id = e1.id
        data = {
            'participants' : '%r,%r'%(e_id, 12)
        }
        result = self.app.post('/api/events/%r'%(e1.id), data=data)
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val["item"],1)
        self.assertEqual(dict_val["success"], True)
        eps = EventParticipant.query.filter_by(event_id=e_id).all()
        self.assertEqual(len(eps), 1)
        self.assertEqual(eps[0].participant.username, 'uname131')

    def test_all_event_participants_for_response_with_inserted_data(self):
        now = datetime.now()
        e1 = Event(title='Event 9s', description='Some desc 9', event_start=now, event_end=now)
        u1 = User(first_name='User12', last_name='Last53', username='uname31', password='pas3232')
        self.test_db.session.add(e1)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        e_id = e1.id
        u_id = u1.id

        ep1 = EventParticipant(event_id=e_id, participant_id=u_id)
        self.test_db.session.add(ep1)
        self.test_db.session.commit()

        result = self.app.get('/api/events/%r'%(e1.id))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]),1)
        self.assertEqual(dict_val["success"], True)
        self.assertEqual(dict_val["items"][0]["firstName"], u1.first_name)
        self.assertEqual(dict_val["items"][0]["lastName"], u1.last_name)

if __name__ == '__main__':
    unittest.main()
