import json
from tests.base_test import BaseTest
import unittest
import tempfile
from app.models.office import User, Campus, Location
import time
from io import BytesIO

class LocationManagerTests(BaseTest):

    def test_all_locations_without_campus_for_response_with_inserted_data(self):
        l1 = Location(latitude=12.32434, longitude=56.4324)
        l2 = Location(latitude=15.32434, longitude=57.4324)
        self.test_db.session.add(l1)
        self.test_db.session.add(l2)
        self.test_db.session.commit()

        result = self.app.get('/api/locations')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 2)
        self.assertEqual(dict_val["items"][0]["latitude"], l1.latitude)
        self.assertIsNone(dict_val["items"][0]["campus"])
        self.assertEqual(dict_val["items"][1]["longitude"], l2.longitude)
        self.assertIsNone(dict_val["items"][1]["campus"])
        self.assertEqual(dict_val["success"], True)


    def test_all_campus_for_response_with_inserted_data(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        c2 = Campus(latitude=15.32434, longitude=57.4324, name='Some Campus2')
        self.test_db.session.add(c1)
        self.test_db.session.add(c2)
        self.test_db.session.commit()

        result = self.app.get('/api/campus')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 2)
        self.assertEqual(dict_val["items"][0]["name"], c1.name)
        self.assertEqual(dict_val["items"][1]["name"], c2.name)
        self.assertEqual(dict_val["success"], True)

    def test_all_locations_with_campus_for_response_with_inserted_data(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        i_c1 = Campus.query.filter_by(latitude=c1.latitude, longitude=c1.longitude, name=c1.name).first()

        l1 = Location(latitude=12.32434, longitude=56.4324, campus_id=i_c1.id)
        self.test_db.session.add(l1)
        self.test_db.session.commit()
        result = self.app.get('/api/locations')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 1)
        self.assertEqual(dict_val["items"][0]["latitude"], l1.latitude)
        self.assertIsNotNone(dict_val["items"][0]["campus"])
        self.assertEqual(dict_val["items"][0]["campus"]["name"], c1.name)
        self.assertEqual(dict_val["success"], True)

    def test_add_location_should_fail_invalid_data(self):
        camp = Campus(name='Campus5', latitude=12.454, longitude=43.23234)
        camp.save()
        data = {
            'name': 'Loc5',
            'latitude': 34.111,
            'campusId' : camp.id
        }
        result = self.app.post('/api/locations',data=data)
        self.assertEqual(result.status_code, 400)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], 'Missing required fields!')
        self.assertEqual(dict_val["success"], False)
        locations = Location.query.all()
        self.assertEqual(len(locations), 0)

    def test_add_location_with_valid_data(self):
        camp = Campus(name='Campus4', latitude=12.454, longitude=43.23234)
        camp.save()
        data = {
            'name': 'Loc4',
            'latitude': 34.111,
            'longitude' : 43.233,
            'campusId' : camp.id
        }
        result = self.app.post('/api/locations',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["name"], data['name'])
        self.assertEqual(dict_val["item"]["latitude"], data['latitude'])
        self.assertEqual(dict_val["success"], True)
        locations = Location.query.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].longitude,  data['longitude'])


    def test_upload_locations_through_endpoint(self):
        file_content = b'[{"id": 1, "name": "loc1", "latitude": 62.64654, "longitude": 63.54465}]'
        data = {}
        data['locations'] = (BytesIO(file_content), 'locations.json')
        result = self.app.post('/api/locations/upload',
                            buffered=True,
                            content_type='multipart/form-data',data=data)
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['success'], True)
        self.assertEqual(dict_val['count'], 1)
        locations = Location.query.all()
        self.assertEqual(len(locations), 1)
        self.assertEqual(locations[0].name, 'loc1')


    def test_download_locations_through_endpoint(self):
        new_loc = Location(name='loc2',latitude=62.64654, longitude=63.54465, campus_id = 0)
        new_loc.save()
        result = self.app.get('/api/locations/download')
        content = b''
        for i in result.response:
            content = content + i
        dict_items = json.loads(content.decode().replace("'", '"'))
        # dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.mimetype, 'application/json')
        self.assertEqual(len(dict_items), 1)
        self.assertEqual(dict_items[0]['name'], 'loc2')

    def test_add_campus_should_fail_invalid_data(self):
        data = {
            'name': 'Campus6',
            'latitude': 34.111
        }
        result = self.app.post('/api/campus',data=data)
        self.assertEqual(result.status_code, 400)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], 'Missing required fields!')
        self.assertEqual(dict_val["success"], False)
        campus = Campus.query.all()
        self.assertEqual(len(campus), 0)

    def test_add_campus_with_valid_data(self):
        data = {
            'name': 'Campus8',
            'latitude': 34.111,
            'longitude' : 43.23
        }
        result = self.app.post('/api/campus',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["name"], data['name'])
        self.assertEqual(dict_val["item"]["latitude"], data['latitude'])
        self.assertEqual(dict_val["success"], True)
        campus = Campus.query.all()
        self.assertEqual(len(campus), 1)
        self.assertEqual(campus[0].longitude,  data['longitude'])


    def test_upload_campus_through_endpoint(self):
        file_content = b'[{"id": 1, "name": "loc1", "latitude": 62.64654, "longitude": 63.54465}]'
        data = {}
        data['campus'] = (BytesIO(file_content), 'campus.json')
        result = self.app.post('/api/campus/upload',
                            buffered=True,
                            content_type='multipart/form-data',data=data)
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['success'], True)
        self.assertEqual(dict_val['count'], 1)
        campus = Campus.query.all()
        self.assertEqual(len(campus), 1)
        self.assertEqual(campus[0].name, 'loc1')


    def test_download_campus_through_endpoint(self):
        new_loc = Campus(name='loc2',latitude=62.64654, longitude=63.54465 )
        new_loc.save()
        result = self.app.get('/api/campus/download')
        content = b''
        for i in result.response:
            content = content + i
        dict_items = json.loads(content.decode().replace("'", '"'))
        # dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.mimetype, 'application/json')
        self.assertEqual(len(dict_items), 1)
        self.assertEqual(dict_items[0]['name'], 'loc2')

if __name__ == '__main__':
    unittest.main()
