import os
import sys
import subprocess
from app import myapp

if __name__ == "__main__":
    try:
        subprocess.check_output(['python', 'run-tests.py'])
        # run app if controll crosses without error
        port = int(os.environ.get('PORT', 8090))
        myapp.debug = True
        myapp.run(host='0.0.0.0', port=port) #Start listening
    except subprocess.CalledProcessError:
        sys.exit('failed tests...App not running...')
