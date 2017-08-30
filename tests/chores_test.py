import json
from tests.base_test import BaseTest
import unittest
from app.models.office import User
from app.models.chores import Announcement
import time
from io import BytesIO
import datetime

class ChoresManagerTests(BaseTest):

    def test_all_announcements_for_response_with_inserted_data(self):
        now = datetime.datetime.now()
        a1 = Announcement(title='Announcement1', description='Some desc 1', category='food', valid_from=now, valid_till=now)
        a2 = Announcement(title='Announcement2', description='Some desc 2', category='emergency', valid_from=now, valid_till=now)

        self.test_db.session.add(a1)
        self.test_db.session.add(a2)
        self.test_db.session.commit()

        result = self.app.get('/api/announcements')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 2)
        self.assertEqual(dict_val["items"][0]["title"], a1.title)
        self.assertEqual(dict_val["items"][1]["title"], a2.title)
        self.assertEqual(dict_val["success"], True)

    def test_add_announcement_with_valid_data(self):
        now = datetime.datetime.now()
        data = {
        'title' : 'Announcement3',
        'description' : 'Some announcements 3',
        'category' : 'food',
        'validFrom' : now.timestamp(),
        'validTo' : now.timestamp()
        }
        result = self.app.post('/api/announcements',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["title"], data['title'])
        self.assertEqual(dict_val["item"]["validFrom"], data['validFrom'])
        self.assertEqual(dict_val["success"], True)
        announcements = Announcement.query.all()
        self.assertEqual(announcements[0].valid_till, now)
        self.assertEqual(announcements[0].description, data['description'])

if __name__ == '__main__':
    unittest.main()
