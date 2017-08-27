import json
from tests.base_test import BaseTest
import unittest
import tempfile
from app.models.office import User, Campus, Location
import time


class UserManagerTests(BaseTest):

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'Welcome to office management system')

    def test_all_users_for_empty_response(self):
        result = self.app.get('/api/users')
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 0)
        self.assertEqual(dict_val["success"], True)

    def test_all_users_without_location_for_response_with_inserted_data(self):
        u1 = User(first_name='user1', last_name='last1', username='uname1', password='password1')
        u2 = User(first_name='user2', last_name='last2', username='uname2', password='password2')
        self.test_db.session.add(u1)
        self.test_db.session.add(u2)
        self.test_db.session.commit()

        result = self.app.get('/api/users')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 2)
        self.assertEqual(dict_val["items"][0]["first_name"], u1.first_name)
        self.assertIsNone(dict_val["items"][0]["location"])
        self.assertEqual(dict_val["items"][1]["last_name"], u2.last_name)
        self.assertIsNone(dict_val["items"][1]["location"])
        self.assertEqual(dict_val["success"], True)

    def test_all_users_with_location_without_campus_for_response_with_inserted_data(self):
        l1 = Location(latitude=12.32434, longitude=56.4324)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        i_l1 = Location.query.filter_by(latitude=l1.latitude, longitude=l1.longitude).first()

        u1 = User(first_name='user1', last_name='last1', username='uname1', password='password1', location_id=i_l1.id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        result = self.app.get('/api/users')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 1)
        self.assertEqual(dict_val["items"][0]["first_name"], u1.first_name)
        self.assertIsNotNone(dict_val["items"][0]["location"])
        self.assertEqual(dict_val["items"][0]["location"]["latitude"], l1.latitude)
        self.assertEqual(dict_val["success"], True)

    def test_all_users_with_location_with_campus_for_response_with_inserted_data(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        i_c1 = Campus.query.filter_by(latitude=c1.latitude, longitude=c1.longitude, name=c1.name).first()

        l1 = Location(latitude=12.32434, longitude=56.4324, campus_id=i_c1.id)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        i_l1 = Location.query.filter_by(latitude=l1.latitude, longitude=l1.longitude).first()

        u1 = User(first_name='user1', last_name='last1', username='uname1', password='password1', location_id=i_l1.id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        result = self.app.get('/api/users')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 1)
        self.assertEqual(dict_val["items"][0]["first_name"], u1.first_name)
        self.assertIsNotNone(dict_val["items"][0]["location"])
        self.assertEqual(dict_val["items"][0]["location"]["latitude"], l1.latitude)
        self.assertIsNotNone(dict_val["items"][0]["location"]["campus"])
        self.assertIsNotNone(dict_val["items"][0]["location"]["campus"]["name"], c1.name)
        self.assertEqual(dict_val["success"], True)


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

    # def test_create_alert_when_giving_valid_input(self):
    #     result = self.app.put('/api/alerts',
    #                           data={'reference_id': 'reference_id_3', 'delay': 1, 'description': 'description 3'})
    #     time.sleep(3)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(result.status_code, 201)
    #     self.assertEqual(dict_val['success'], True)
    #
    # def test_create_alert_when_giving_missing_input(self):
    #     result = self.app.put('/api/alerts',
    #                           data={'reference_id': 'reference_id_4', 'description': 'description 4'})
    #     time.sleep(2)
    #     self.assertEqual(result.status_code, 400)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], False)
    #     self.assertEqual(dict_val['message'], 'Invalid/Empty fields')
    #
    # def test_create_alert_when_giving_existing_reference_id(self):
    #     alert1 = Alert(description="description 1", reference_id="reference_1", delay=10, status="STARTED")
    #     db.session.add(alert1)
    #     db.session.commit()
    #     result = self.app.put('/api/alerts',
    #                           data={'reference_id': 'reference_1', 'delay': 1, 'description': 'description 1'})
    #     time.sleep(2)
    #     self.assertEqual(result.status_code, 400)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], False)
    #     self.assertEqual(dict_val['message'], 'Duplicate reference Id')
    #
    # def test_clear_alert_when_giving_valid_reference_id_with_started_status(self):
    #     alert1 = Alert(description="description 1", reference_id="reference_1", delay=10, status="STARTED")
    #     db.session.add(alert1)
    #     db.session.commit()
    #     result = self.app.post('/api/alerts/reference_1')
    #
    #     actual_alert = Alert.query.filter_by(reference_id='reference_1').first()
    #
    #     self.assertEqual(result.status_code, 201)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], True)
    #     self.assertEqual(actual_alert.status, 'COMPLETED')
    #
    # def test_clear_alert_when_giving_valid_reference_id_with_pending_status(self):
    #     alert1 = Alert(description="description 2", reference_id="reference_2", delay=10, status="PENDING")
    #     db.session.add(alert1)
    #     db.session.commit()
    #     result = self.app.post('/api/alerts/reference_2')
    #
    #     actual_alert = Alert.query.filter_by(reference_id='reference_2').first()
    #
    #     self.assertEqual(result.status_code, 201)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], True)
    #     self.assertEqual(actual_alert.status, 'COMPLETED')
    #
    # def test_clear_alert_rejects_when_giving_invalid_reference_id(self):
    #
    #     result = self.app.post('/api/alerts/reference_1')
    #     self.assertEqual(result.status_code, 400)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], False)
    #     self.assertEqual(dict_val['message'], 'Invalid reference id')
    #
    # def test_clear_alert_when_the_alert_is_still_in_delay_period(self):
    #     self.app.put('/api/alerts',
    #                  data={'reference_id': 'reference_id_5', 'description': 'description 5', 'delay': 5})
    #     time.sleep(2)
    #     result = self.app.post('/api/alerts/reference_id_5')
    #     self.assertEqual(result.status_code, 201)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], True)
    #     time.sleep(5)
    #     actual_alert = Alert.query.filter_by(reference_id='reference_id_5').first()
    #     self.assertEqual(actual_alert.status, 'COMPLETED')
    #

if __name__ == '__main__':
    unittest.main()
