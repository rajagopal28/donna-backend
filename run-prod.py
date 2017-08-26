import os
import sys
from app import myapp

from tests import run as run_tests

result = run_tests()
if (len(result.errors) == 0 & len(result.failures) == 0 ):
    port = int(os.environ.get('PORT', 8090))
    myapp.debug = False
    myapp.run(host='0.0.0.0', port=port) #Start listening
else:
    sys.exit('failed tests...')
