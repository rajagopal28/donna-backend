import json
import unittest
import time
from io import BytesIO

from tests.base_test import BaseTest
from app.models.office import User, Campus, Location

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
        self.assertEqual(dict_val["items"][0]["firstName"], u1.first_name)
        self.assertIsNone(dict_val["items"][0]["location"])
        self.assertEqual(dict_val["items"][1]["lastName"], u2.last_name)
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
        self.assertEqual(dict_val["items"][0]["firstName"], u1.first_name)
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
        self.assertEqual(dict_val["items"][0]["firstName"], u1.first_name)
        self.assertIsNotNone(dict_val["items"][0]["location"])
        self.assertEqual(dict_val["items"][0]["location"]["latitude"], l1.latitude)
        self.assertIsNotNone(dict_val["items"][0]["location"]["campus"])
        self.assertIsNotNone(dict_val["items"][0]["location"]["campus"]["name"], c1.name)
        self.assertEqual(dict_val["success"], True)


    def test_all_users_in_campus_with_location_with_campus_for_response_with_inserted_data(self):
        c1 = Campus(latitude=12.32434, longitude=56.4324, name='Some Campus1')
        self.test_db.session.add(c1)
        self.test_db.session.commit()

        i_c1 = Campus.query.filter_by(latitude=c1.latitude, longitude=c1.longitude, name=c1.name).first()

        l1 = Location(latitude=12.32434, longitude=56.4324, campus_id=i_c1.id)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        i_l1 = Location.query.filter_by(latitude=l1.latitude, longitude=l1.longitude).first()

        u1 = User(first_name='user1', last_name='last1', username='uname1', password='password1', location_id=i_l1.id)
        u2 = User(first_name='user2', last_name='last2', username='uname2', password='password2')
        self.test_db.session.add(u1)
        self.test_db.session.add(u2)
        self.test_db.session.commit()
        result = self.app.get('/api/users?campusId='+str(i_c1.id))
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 1)
        self.assertEqual(dict_val["items"][0]["firstName"], u1.first_name)
        self.assertIsNotNone(dict_val["items"][0]["location"])
        self.assertEqual(dict_val["items"][0]["location"]["latitude"], l1.latitude)
        self.assertIsNotNone(dict_val["items"][0]["location"]["campus"])
        self.assertIsNotNone(dict_val["items"][0]["location"]["campus"]["name"], c1.name)
        self.assertEqual(dict_val["success"], True)


    def test_no_users_in_campus_with_location_no_campus_for_response_with_inserted_data(self):
        l1 = Location(latitude=12.32434, longitude=56.4324)
        self.test_db.session.add(l1)
        self.test_db.session.commit()

        i_l1 = Location.query.filter_by(latitude=l1.latitude, longitude=l1.longitude).first()

        u1 = User(first_name='user1', last_name='last1', username='uname1', password='password1', location_id=i_l1.id)
        self.test_db.session.add(u1)
        self.test_db.session.commit()
        result = self.app.get('/api/users?campusId=1')
        dict_val = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(dict_val["items"]), 0)
        self.assertEqual(dict_val["success"], True)



    def test_add_user_should_fail_invalid_data(self):
        loc = Location(name='Loc4', latitude=12.454, longitude=43.23234)
        loc.save()
        data = {
            'firstName' : 'User4',
            'username' : 'uname4',
            'password' : 'pass4',
            'locationId': loc.id
        }
        result = self.app.post('/api/users',data=data)
        self.assertEqual(result.status_code, 400)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], 'Missing required fields!')
        self.assertEqual(dict_val["success"], False)
        users = User.query.all()
        self.assertEqual(len(users), 0)

    def test_add_user_with_valid_data(self):
        loc = Location(name='Loc4', latitude=12.454, longitude=43.23234)
        loc.save()
        data = {
            'firstName' : 'User4',
            'lastName' : 'Last4',
            'username' : 'uname4',
            'password' : 'pass4',
            'locationId': loc.id
        }
        result = self.app.post('/api/users',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["firstName"], data['firstName'])
        self.assertEqual(dict_val["item"]["username"], data['username'])
        self.assertEqual(dict_val["success"], True)
        users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].last_name,  data['lastName'])

    def test_login_pass_with_valid_data(self):
        u1 = User(first_name='user5', last_name='last5', username='uname5', password='password5')
        u1.save()
        data = {
            'username' : u1.username,
            'password' : u1.password
        }
        result = self.app.post('/api/users/login',data=data)
        self.assertEqual(result.status_code, 200)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["item"]["firstName"], u1.first_name)
        self.assertEqual(dict_val["item"]["username"], u1.username)
        self.assertEqual(dict_val["success"], True)


    def test_login_pass_with_invalid_data(self):
        u1 = User(first_name='user5', last_name='last5', username='uname5', password='password5')
        u1.save()
        data = {
            'username' : u1.username
        }
        result = self.app.post('/api/users/login',data=data)
        self.assertEqual(result.status_code, 401)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], 'Missing required fields!')
        self.assertEqual(dict_val["success"], False)


    def test_login_pass_with_invalid_credential_data(self):
        u1 = User(first_name='user5', last_name='last5', username='uname5', password='password5')
        u1.save()
        data = {
            'username' : u1.username,
            'password' : 'wrongpass'
        }
        result = self.app.post('/api/users/login',data=data)
        self.assertEqual(result.status_code, 403)
        dict_val = json.loads(result.data)
        self.assertEqual(dict_val["message"], 'Authentication Failed!')
        self.assertEqual(dict_val["success"], False)

    def test_upload_users_through_endpoint_complete_upload(self):
        file_content = b'[{"id": 1, "firstName": "User1", "lastName": "Last1", "username": "userlast1", "password": "pass1"}]'
        data = {}
        data['users'] = (BytesIO(file_content), 'users.json')
        result = self.app.post('/api/users/upload',
                            buffered=True,
                            content_type='multipart/form-data',data=data)
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['success'], True)
        self.assertEqual(dict_val['count'], 1)
        users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].first_name, 'User1')
        self.assertEqual(users[0].last_name, 'Last1')


    def test_upload_users_through_endpoint_partial_upload(self):
        file_content = b'[{"id": 1, "firstName": "User1", "lastName": "Last1", "username": "userlast1", "password": "pass1"},{"id": 2, "firstName": "User7", "lastName": "Last8"}]'
        data = {}
        data['users'] = (BytesIO(file_content), 'users.json')
        result = self.app.post('/api/users/upload',
                            buffered=True,
                            content_type='multipart/form-data',data=data)
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['success'], False)
        self.assertEqual(dict_val['count'], 1)
        users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].first_name, 'User1')
        self.assertEqual(users[0].last_name, 'Last1')

    def test_download_users_through_endpoint(self):
        new_user = User(first_name='User2', last_name='Last2', username='uname2', password='pass2')
        new_user.save()
        result = self.app.get('/api/users/download')
        content = b''
        for i in result.response:
            content = content + i
        dict_items = json.loads(content.decode().replace("'", '"'))
        # dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.mimetype, 'application/json')
        self.assertEqual(len(dict_items), 1)
        self.assertEqual(dict_items[0]['firstName'], 'User2')
        self.assertEqual(dict_items[0]['lastName'], 'Last2')

    def test_find_user_with_valid_id(self):
        new_user = User(first_name='User2', last_name='Last2', username='uname2', password='pass2')
        new_user.save()
        result = self.app.get('/api/users/%r'%(new_user.id))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['success'], True)
        self.assertEqual(dict_val['item']['firstName'], new_user.first_name)
        self.assertEqual(dict_val['item']['username'], new_user.username)

    def test_fail_for_user_with_invalid_id(self):
        result = self.app.get('/api/users/12')
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(dict_val['success'], False)
        self.assertEqual(dict_val['message'], 'Requested Record Not Available!')

    def test_succeed_deleting_user_with_valid_id(self):
        new_user = User(first_name='User2', last_name='Last2', username='uname2', password='pass2')
        new_user.save()
        result = self.app.delete('/api/users/%r'%(new_user.id))
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(dict_val['success'], True)
        self.assertEqual(dict_val['item']['firstName'], new_user.first_name)
        self.assertEqual(dict_val['item']['username'], new_user.username)
        users = User.query.all()
        self.assertEqual(len(users), 0)

    def test_fail_to_delete_user_with_invalid_id(self):
        result = self.app.delete('/api/users/12')
        dict_val = json.loads(result.data)
        self.assertEqual(result.status_code, 404)
        self.assertEqual(dict_val['success'], False)
        self.assertEqual(dict_val['message'], 'Requested Record Not Available!')
if __name__ == '__main__':
    unittest.main()
