import os
import sys
import subprocess

if __name__ == "__main__":
    # try:
    #     subprocess.check_output(['python', 'run-tests.py'])
    #     # run app if controll crosses without error
    #
    #     from app import myapp
    #     port = int(os.environ.get('PORT', 8090))
    #     myapp.debug = True
    #     myapp.run(host='0.0.0.0', port=port) #Start listening
    # except subprocess.CalledProcessError:
    #     sys.exit('failed tests...App not running...')
    from app import myapp
    port = int(os.environ.get('PORT', 8090))
    myapp.debug = True
    myapp.run(host='0.0.0.0', port=port) #Start listening
