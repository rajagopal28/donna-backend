import sys
from tests import run as run_tests

if __name__ == "__main__":
    result = run_tests()
    tests_clear = (len(result.errors) == 0 & len(result.failures) == 0)
    if not tests_clear:
        sys.exit('failed test cases...')
