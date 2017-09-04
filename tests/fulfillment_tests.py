import json
from tests.base_test import BaseTest
import unittest
from app.models.office import User, Location
from app.models.chores import Announcement, Event, EventParticipant
import time
from io import BytesIO
from datetime import datetime, timedelta

class FulfillmentManagerTests(BaseTest):

    def test_should_return_input_payload_if_no_action_defined(self):
        payload_data = {
            'status' : {
                'errorType': 'success',
                'code': 200
            },'result': {
                'parameters': {
                    'city': 'Rome',
                    'name': 'Ana'
                },
                'contexts': [],
                'action': 'greetings'
            }
        }
        result = self.app.post('/api/ai/fulfillment', content_type='application/json', data=json.dumps(payload_data))
        print (result.data)
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val, payload_data)


    def test_should_not_process_meeting_for_invalid_input_with_auth_in_action_schedule_meeting(self):
        payload_data = {
            'status' : {
                'errorType': 'success',
                'code': 200
            },
            'result': {
                'parameters': {
                    'campus-location' : 'camp1',
                    'office-user' : 'user1',
                    'date' : '2017-09-08',
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
        self.assertEqual(dict_val['speech'], 'Oops!! Missing required meeting info. Please try again')
        self.assertEqual(dict_val['displayText'], 'Oops!! Missing required meeting info. Please try again')


    def test_should_not_process_meeting_for_valid_input_without_auth_in_action_schedule_meeting(self):
        payload_data = {
            'status' : {
                'errorType': 'success',
                'code': 200
            },
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
            'status' : {
                'errorType': 'success',
                'code': 200
            },
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

    def test_should_return_processed_data_for_valid_and_data_input_in_action_schedule_meeting(self):

        u1 = User(first_name='user2', last_name='last2', username='uname2', password='password2')
        l1 = Location(latitude=15.32434, longitude=57.432, name='loc1')
        self.test_db.session.add(u1)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        payload_data = {
            'status' : {
                'errorType': 'success',
                'code': 200
            },
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


if __name__ == '__main__':
    unittest.main()
