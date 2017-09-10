import json
from tests.base_test import BaseTest
import unittest
from app.models.office import User, Location, Campus
from app.models.chores import Announcement, Event, EventParticipant

from app.services.chat_fullfilment_service import dstr
import time
from io import BytesIO
from datetime import datetime, timedelta

class FulfillmentManagerTests(BaseTest):

    def test_should_return_input_payload_if_no_action_defined(self):
        payload_data = {
            'result': {
                'parameters': {
                    'city': 'Rome',
                    'name': 'Ana'
                },
                'contexts': [],
                'action': 'greetings'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        # print (result.data)
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val, payload_data)


    def test_should_not_process_meeting_for_invalid_input_with_auth_in_action_schedule_meeting(self):
        payload_data = {
            'result': {
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'parameters' : {
                    'some-param' : 'some-value'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname1'
                    }
                }],
                'action': 'schedule-meeting-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['speech'], 'Oops!! Missing required meeting info. Please try again')
        self.assertEqual(dict_val['displayText'], 'Oops!! Missing required meeting info. Please try again')


    def test_should_not_process_meeting_for_valid_input_without_auth_in_action_schedule_meeting(self):
        payload_data = {
            'result': {
                'parameters': {
                    'campus-location' : 'camp1',
                    'office-user' : 'user1',
                    'date' : '2017-09-08',
                    'time' : '13:30:00'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [],
                'action': 'schedule-meeting-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['speech'], 'Not authenticated to Add Event!!')
        self.assertEqual(dict_val['displayText'], 'Not authenticated to Add Event!!')


    def test_should_return_processed_data_for_valid_input_and_data_in_action_schedule_meeting(self):
        payload_data = {
            'result': {
                'parameters': {
                    'campus-location' : 'camp1',
                    'office-user' : 'user1',
                    'date' : '2017-09-08',
                    'time' : '13:30:00'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname1'
                    }
                }],
                'action': 'schedule-meeting-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['speech'], 'Not Added Event!!')


    def test_should_return_processed_data_for_valid_input_default_date_place_and_data_in_action_schedule_meeting(self):
        l1 = Location(latitude=15.32434, longitude=57.432, name='loc1')
        self.test_db.session.add(l1)
        self.test_db.session.commit()
        u1 = User(first_name='user2', last_name='last2', username='uname2', password='password2', location_id=l1.id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        u1_id = u1.id

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location' : 'your_location',
                    'office-user' : 'user2',
                    'date' : 'today',
                    'time' : '13:30:00'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname2'
                    }
                }],
                'action': 'schedule-meeting-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['speech'], 'Added!' + payload_data['result']['fulfillment']['speech'])
        self.assertEqual(dict_val['displayText'], 'Added!' + payload_data['result']['fulfillment']['speech'])
        meetings = Event.query.all()
        self.assertEqual(len(meetings), 1)
        self.assertEqual(meetings[0].title, 'user2\'s meeting with user2 at loc1')
        self.assertEqual(len(meetings[0].event_participants), 1)
        self.assertEqual(meetings[0].event_participants[0].participant_id, u1_id)


    def test_should_return_processed_data_for_valid_and_data_input_in_action_schedule_meeting(self):

        u1 = User(first_name='user2', last_name='last2', username='uname2', password='password2')
        l1 = Location(latitude=15.32434, longitude=57.432, name='loc1')
        self.test_db.session.add(u1)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        u1_id = u1.id

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location' : 'loc1',
                    'office-user' : 'user2',
                    'date' : '2017-09-08',
                    'time' : '13:30:00'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname2'
                    }
                }],
                'action': 'schedule-meeting-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['speech'], 'Added!' + payload_data['result']['fulfillment']['speech'])
        self.assertEqual(dict_val['displayText'], 'Added!' + payload_data['result']['fulfillment']['speech'])
        meetings = Event.query.all()
        self.assertEqual(len(meetings), 1)
        self.assertEqual(meetings[0].title, 'user2\'s meeting with user2 at loc1')
        self.assertEqual(len(meetings[0].event_participants), 1)
        self.assertEqual(meetings[0].event_participants[0].participant_id, u1_id)


    def test_should_process_meeting_for_valid_input_without_auth_in_action_schedule_meeting(self):
        payload_data = {
            'result': {
                'parameters': {
                    'campus-location' : 'camp1',
                    'office-user' : 'user1',
                    'date' : '2017-09-08',
                    'time' : '13:30:00'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [],
                'action': 'schedule-meeting-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['speech'], 'Not authenticated to Add Event!!')
        self.assertEqual(dict_val['displayText'], 'Not authenticated to Add Event!!')


    def test_should_return_processed_data_for_valid_input_auth_and_data_in_action_view_meetings(self):
        now = datetime.now()
        e1 = Event(title='Event 9s', description='Some desc 9', event_start=now, event_end=now)
        e2 = Event(title='Event 12', description='Some desc 12', event_start=now, event_end=now)
        self.test_db.session.add(e1)
        self.test_db.session.add(e2)
        self.test_db.session.commit()
        payload_data = {
            'result': {
                'parameters': {
                    'some-param': 'some-value'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [],
                'action': 'view-meetings-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)

        res_string = ", ".join([(e.title+' From: '+dstr(now)+' Till: '+dstr(now)) for e in [e1, e2]])
        self.assertEqual(dict_val['speech'], res_string)

    def test_should_return_processed_data_for_valid_auth_and_data_input_in_action_view_meetings(self):
        now = datetime.now()
        e1 = Event(title='Event 9s', description='Some desc 9', event_start=now, event_end=now)
        e2 = Event(title='Event 12', description='Some desc 12', event_start=now, event_end=now)
        u1 = User(first_name='User12', last_name='Last53', username='uname31', password='pas3232')
        self.test_db.session.add(e1)
        self.test_db.session.add(e2)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        e_id = e1.id
        u_id = u1.id

        ep1 = EventParticipant(event_id=e_id, participant_id=u_id)
        self.test_db.session.add(ep1)
        self.test_db.session.commit()


        payload_data = {
            'result': {
                'parameters': {
                    'some-param': 'some-value'
                },
                'fulfillment': {
                    'speech': 'Hi Ana! Nice to meet you!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname31'
                    }
                }],
                'action': 'view-meetings-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], (e1.title+' From: '+dstr(now)+' Till: '+dstr(now)))


    def test_should_return_processed_data_for_valid_data_for_user_no_location_in_action_view_person_info(self):
        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232')
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        payload_data = {
            'result': {
                'parameters': {
                    'office-user': 'User22'
                },
                'fulfillment': {
                    'speech': 'Some message for view-person-info-request!'
                },
                'contexts': [],
                'action': 'view-person-info-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], 'User: User22 Last32')


    def test_should_return_processed_data_for_valid_data_for_user_and_location_in_action_view_person_info(self):
        l1 = Location(latitude=12.32434, longitude=56.4324, name="New user loc1111")
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232', location_id=l1.id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        payload_data = {
            'result': {
                'parameters': {
                    'office-user': 'User22'
                },
                'fulfillment': {
                    'speech': 'Some message for view-person-info-request!'
                },
                'contexts': [],
                'action': 'view-person-info-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], 'User: User22 Last32 is located at New user loc1111')
        self.assertEqual(dict_val['data']['web']['parameters']['location']['name'], l1.name)
        self.assertEqual(dict_val['data']['web']['parameters']['location']['latitude'], l1.latitude)
        self.assertEqual(dict_val['parameters']['location']['name'], l1.name)
        self.assertEqual(dict_val['parameters']['location']['latitude'], l1.latitude)


    def test_should_not_processed_data_for_invalid_data_for_view_person_info(self):
        payload_data = {
            'result': {
                'parameters': {
                    'some-param': 'vv121'
                },
                'fulfillment': {
                    'speech': 'Some message for view-person-info-request!'
                },
                'contexts': [],
                'action': 'view-person-info-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], payload_data['result']['fulfillment']['speech'])


    def test_should_redirect_to_action_view_person_info_for_action_view_person_location_info(self):
        l1 = Location(latitude=22.32434, longitude=86.4324, name="New user loc1221")
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232', location_id=l1.id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        payload_data = {
            'result': {
                'parameters': {
                    'office-user': 'User22'
                },
                'fulfillment': {
                    'speech': 'Some message for view-person-info-request!'
                },
                'contexts': [],
                'action': 'view-person-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], 'User: User22 Last32 is located at New user loc1221')
        self.assertEqual(dict_val['data']['web']['parameters']['location']['name'], l1.name)
        self.assertEqual(dict_val['data']['web']['parameters']['location']['latitude'], l1.latitude)
        self.assertEqual(dict_val['parameters']['location']['name'], l1.name)
        self.assertEqual(dict_val['parameters']['location']['latitude'], l1.latitude)

    def test_should_return_processed_data_for_valid_data_for_location_no_campus_in_action_view_location_info(self):
        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc123")
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc123'
                },
                'fulfillment': {
                    'speech': 'Some message for view-location-info-request!'
                },
                'contexts': [],
                'action': 'view-location-info-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        speech_resp = 'Location: %r with co-ordinates(%r, %r)'%(l1.name, str(l1.latitude), str(l1.longitude))
        self.assertEqual(dict_val['speech'], speech_resp)


    def test_should_return_processed_data_for_valid_data_for_location_and_campus_in_action_view_location_info(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        c1_id = c1.id

        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc332", campus_id=c1_id)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc332'
                },
                'fulfillment': {
                    'speech': 'Some message for view-location-info-request!'
                },
                'contexts': [],
                'action': 'view-location-info-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        str_resp = 'Location: %r with co-ordinates(%r, %r) is located at Campus: %r'%(l1.name, str(l1.latitude), str(l1.longitude), c1.name)
        self.assertEqual(dict_val['speech'], str_resp)
        self.assertEqual(dict_val['data']['web']['parameters']['location']['name'], l1.name)
        self.assertEqual(dict_val['data']['web']['parameters']['location']['latitude'], l1.latitude)
        self.assertEqual(dict_val['parameters']['location']['name'], l1.name)
        self.assertEqual(dict_val['parameters']['location']['latitude'], l1.latitude)


    def test_should_not_processed_data_for_invalid_data_for_view_location_info(self):
        payload_data = {
            'result': {
                'parameters': {
                    'some-param': 'vv121'
                },
                'fulfillment': {
                    'speech': 'Some message for view-location-info-request!'
                },
                'contexts': [],
                'action': 'view-location-info-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], payload_data['result']['fulfillment']['speech'])


    def test_should_return_processed_data_for_valid_data_with_food_type_for_announcements(self):
        a1 = Announcement(title='Announcement12meetings', description='some Announcement related to meetings', category='meetings')
        a2 = Announcement(title='Announcement24food', description='some Announcement related to food', category='food')

        self.test_db.session.add(a1)
        self.test_db.session.add(a2)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'event-type': 'food'
                },
                'fulfillment': {
                    'speech': 'Some message for view-office-announcements!'
                },
                'contexts': [],
                'action': 'view-office-announcements'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], 'Announcement24food From:  Till: ')

    def test_should_return_processed_data_for_valid_data_with_non_food_type_for_announcements(self):
        a1 = Announcement(title='Announcement12meetings', description='some Announcement related to meetings', category='meetings')
        a2 = Announcement(title='Announcement24food', description='some Announcement related to food', category='food')

        self.test_db.session.add(a1)
        self.test_db.session.add(a2)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'event-type': 'celebrations'
                },
                'fulfillment': {
                    'speech': 'Some message for view-office-announcements!'
                },
                'contexts': [],
                'action': 'view-office-announcements'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], 'Announcement12meetings From:  Till: , Announcement24food From:  Till: ')


    def test_should_not_processed_data_for_valid_data_with_no_type_for_announcements(self):
        payload_data = {
            'result': {
                'parameters': {
                    'some-param': 'some-value'
                },
                'fulfillment': {
                    'speech': 'Some message for view-office-announcements!'
                },
                'contexts': [],
                'action': 'view-office-announcements'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], payload_data['result']['fulfillment']['speech'])


    def test_should_return_processed_data_for_valid_data_for_location_and_campus_in_action_route_to_location_info(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        c1_id = c1.id

        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc332", campus_id=c1_id)
        l2 = Location(latitude=22.32434, longitude=95.4324, name="loc255", campus_id=c1_id)
        self.test_db.session.add(l1)
        self.test_db.session.add(l2)
        self.test_db.session.commit()

        l1_id = l1.id
        l2_id = l2.id

        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232', location_id=l1_id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc255'
                },
                'fulfillment': {
                    'speech': 'Some message for route-to-location-request!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname39'
                    }
                }],
                'action': 'route-to-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        str_resp = 'Taking you to Location: %r with co-ordinates(%r, %r) is located at Campus: %r'%('loc255', '22.32434', '95.4324', 'Some Campus1')
        self.assertEqual(dict_val['speech'], str_resp)

        self.assertEqual(dict_val['data']['web']['parameters']['fromLocation']['name'],'loc332')
        self.assertEqual(dict_val['data']['web']['parameters']['fromLocation']['latitude'], 12.32434)
        self.assertEqual(dict_val['data']['web']['parameters']['toLocation']['name'],'loc255')
        self.assertEqual(dict_val['data']['web']['parameters']['toLocation']['longitude'], 95.4324)
        self.assertEqual(dict_val['parameters']['fromLocation']['name'], 'loc332')
        self.assertEqual(dict_val['parameters']['fromLocation']['latitude'], 12.32434)
        self.assertEqual(dict_val['parameters']['toLocation']['name'], 'loc255')
        self.assertEqual(dict_val['parameters']['toLocation']['longitude'], 95.4324)

    def test_should_return_processed_data_for_valid_data_for_location_and_campus_diff_campus_in_action_route_to_location_info(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        c1_id = c1.id

        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc332", campus_id=c1_id)
        l2 = Location(latitude=22.32434, longitude=95.4324, name="loc255")
        self.test_db.session.add(l1)
        self.test_db.session.add(l2)
        self.test_db.session.commit()

        l1_id = l1.id
        l2_id = l2.id

        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232', location_id=l1_id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc255'
                },
                'fulfillment': {
                    'speech': 'Some message for route-to-location-request!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname39'
                    }
                }],
                'action': 'route-to-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        str_resp = 'You are not in the same campus to View Routes!'
        self.assertEqual(dict_val['speech'], str_resp)
        self.assertEqual(dict_val['data']['web']['parameters']['fromLocation']['name'],'loc332')
        self.assertEqual(dict_val['data']['web']['parameters']['fromLocation']['latitude'], 12.32434)
        self.assertEqual(dict_val['data']['web']['parameters']['toLocation']['name'],'loc255')
        self.assertEqual(dict_val['data']['web']['parameters']['toLocation']['longitude'], 95.4324)
        self.assertEqual(dict_val['parameters']['fromLocation']['name'], 'loc332')
        self.assertEqual(dict_val['parameters']['fromLocation']['latitude'], 12.32434)
        self.assertEqual(dict_val['parameters']['toLocation']['name'], 'loc255')
        self.assertEqual(dict_val['parameters']['toLocation']['longitude'], 95.4324)
        self.assertEqual(dict_val['parameters']['noRoute'], 'true')

    def test_should_return_unprocessed_data_for_valid_data_for_location_and_no_user_diff_campus_in_action_route_to_location_info(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        c1_id = c1.id

        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc332", campus_id=c1_id)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc255'
                },
                'fulfillment': {
                    'speech': 'Some message for route-to-location-request!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname39'
                    }
                }],
                'action': 'route-to-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        str_resp = 'Invalid User Token!'
        self.assertEqual(dict_val['speech'], str_resp)

    def test_should_return_not_process_data_for_invalid_data_for_no_location_in_action_route_to_location_info(self):

        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc332")
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        l1_id = l1.id
        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232', location_id=l1_id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc255'
                },
                'fulfillment': {
                    'speech': 'Some message for route-to-location-request!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname39'
                    }
                }],
                'action': 'route-to-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        str_resp = 'Not a valid Location'
        self.assertEqual(dict_val['speech'], str_resp)


    def test_should_return_not_process_data_for_invalid_data_for_no_location_in_action_route_to_location_info(self):

        l1 = Location(latitude=12.32434, longitude=56.4324, name="loc332")
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        u1 = User(first_name='User22', last_name='Last32', username='uname39', password='pas3232')
        self.test_db.session.add(u1)
        self.test_db.session.commit()

        payload_data = {
            'result': {
                'parameters': {
                    'campus-location': 'loc332'
                },
                'fulfillment': {
                    'speech': 'Some message for route-to-location-request!'
                },
                'contexts': [{
                    'name' : 'auth',
                    'parameters' : {
                        'token' : 'uname39'
                    }
                }],
                'action': 'route-to-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        str_resp = 'User has no location to route to!'
        self.assertEqual(dict_val['speech'], str_resp)

    def test_should_not_processed_data_for_invalid_data_for_route_to_location_info(self):
        payload_data = {
            'result': {
                'parameters': {
                    'some-param': 'vv121'
                },
                'fulfillment': {
                    'speech': 'Some message for route-to-location-request!'
                },
                'contexts': [],
                'action': 'route-to-location-request'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        # print(dict_val)
        self.assertEqual(dict_val['speech'], payload_data['result']['fulfillment']['speech'])

if __name__ == '__main__':
    unittest.main()
