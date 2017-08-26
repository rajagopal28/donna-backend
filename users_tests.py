import json
from app import myapp, db
import unittest
import tempfile
from app.models.office import User
import time


class UserManagerTests(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=True)
        print (self.temp_db_file.name)
        myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.temp_db_file.name
        myapp.config['TESTING'] = True
        self.app = myapp.test_client()
        db.init_app(myapp)
        db.create_all()

    @classmethod
    def tearDown(self):
        if self.temp_db_file:
            self.temp_db_file.close
            self.temp_db_file.delete
        if db:
            db.session.remove()
            db.drop_all()

    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.myapp.get('/')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, 'Welcome to office management system')

    def test_all_users_for_empty_response(self):
        result = self.myapp.get('/api/users')
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 0)
        self.assertEqual(dict_val["success"], True)
    #
    # def test_all_alerts_for_response_with_inserted_data_with_status_started(self):
    #     alert1 = Alert(description="description 1", reference_id="reference_1", delay=10, status="STARTED")
    #     alert2 = Alert(description="description 2", reference_id="reference_2", delay=20, status="STARTED")
    #     db.session.add(alert1)
    #     db.session.add(alert2)
    #     db.session.commit()
    #
    #     result = self.myapp.get('/api/alerts')
    #     dict_val = json.loads(result.data)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertEqual(len(dict_val["items"]), 2)
    #     self.assertEqual(dict_val["items"][0]["reference_id"], alert1.reference_id)
    #     self.assertEqual(dict_val["items"][1]["reference_id"], alert2.reference_id)
    #     self.assertEqual(dict_val["success"], True)
    #
    # def test_create_alert_when_giving_valid_input(self):
    #     result = self.myapp.put('/api/alerts',
    #                           data={'reference_id': 'reference_id_3', 'delay': 1, 'description': 'description 3'})
    #     time.sleep(3)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(result.status_code, 201)
    #     self.assertEqual(dict_val['success'], True)
    #
    # def test_create_alert_when_giving_missing_input(self):
    #     result = self.myapp.put('/api/alerts',
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
    #     result = self.myapp.put('/api/alerts',
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
    #     result = self.myapp.post('/api/alerts/reference_1')
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
    #     result = self.myapp.post('/api/alerts/reference_2')
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
    #     result = self.myapp.post('/api/alerts/reference_1')
    #     self.assertEqual(result.status_code, 400)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], False)
    #     self.assertEqual(dict_val['message'], 'Invalid reference id')
    #
    # def test_clear_alert_when_the_alert_is_still_in_delay_period(self):
    #     self.myapp.put('/api/alerts',
    #                  data={'reference_id': 'reference_id_5', 'description': 'description 5', 'delay': 5})
    #     time.sleep(2)
    #     result = self.myapp.post('/api/alerts/reference_id_5')
    #     self.assertEqual(result.status_code, 201)
    #     dict_val = json.loads(result.data)
    #     self.assertEqual(dict_val['success'], True)
    #     time.sleep(5)
    #     actual_alert = Alert.query.filter_by(reference_id='reference_id_5').first()
    #     self.assertEqual(actual_alert.status, 'COMPLETED')
    #

if __name__ == '__main__':
    unittest.main()
