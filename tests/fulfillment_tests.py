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


    def test_should_return_processed_data_for_valid_input_in_action_schedule_meeting(self):
        payload_data = {
            'status' : {
                'errorType': 'success',
                'code': 200
            },
            'result': {
                'parameters': {
                    'city': 'Rome',
                    'name': 'Ana'
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
        self.assertEqual(dict_val['speech'], payload_data['result']['fulfillment']['speech'])
        self.assertEqual(dict_val['displayText'], payload_data['result']['fulfillment']['speech'])

if __name__ == '__main__':
    unittest.main()
