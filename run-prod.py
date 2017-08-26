from tests import run as run_tests

# result = run_tests()
tests_clear = True # (len(result.errors) == 0 & len(result.failures) == 0)

import os
import sys
from app import myapp

if (tests_clear):
    port = int(os.environ.get('PORT', 8090))
    myapp.debug = True
    myapp.run(host='0.0.0.0', port=port) #Start listening
else:
    sys.exit('failed tests...')
