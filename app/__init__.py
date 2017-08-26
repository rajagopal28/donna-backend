from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

myapp = Flask(__name__)

# Include config from config.py
myapp.config.from_pyfile('config.py')

db = SQLAlchemy(myapp)

import app.views.users

db.create_all()
db.session.commit()



if __name__ == '__main__':
    print('Hanyasiyooo')
    myapp.run()
