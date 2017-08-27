from app import myapp, db
import unittest
import tempfile


class BaseTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=True)
        # print('setting up...')
        print (self.temp_db_file.name) # .replace('RMUTHU~1', 'rmuthuchidambara')
        self.user_db = myapp.config['SQLALCHEMY_DATABASE_URI']
        myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.temp_db_file.name
        myapp.config['TESTING'] = True
        self.app = myapp.test_client()
        db.init_app(myapp)
        db.create_all()
        self.test_db = db

    @classmethod
    def tearDown(self):
        # print('tearing down...')
        if self.temp_db_file:
            self.temp_db_file.close
            self.temp_db_file.delete
        if db:
            db.session.remove()
            db.drop_all()
        myapp.config['SQLALCHEMY_DATABASE_URI'] = self.user_db
