import os
from app import myapp

port = int(os.environ.get('PORT', 8090))
myapp.debug = False
myapp.run(host='0.0.0.0', port=port) #Start listening
