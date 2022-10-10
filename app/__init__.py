import os
from flask import Flask
# Use this import format
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

myapp = Flask(__name__)
CORS(myapp)

# Include config from config.py
myapp.config.from_pyfile('config.py')

db = SQLAlchemy(myapp)

import app.views.users
import app.views.locations
import app.views.chores
db.create_all()
db.session.commit()



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8090))
    myapp.run(host='0.0.0.0', port=port) #Start listening
