from tests.users_tests import UserManagerTests
from unittest import TestLoader, TextTestRunner, TestSuite

if __name__ == "__main__":
    run()

def run():
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(UserManagerTests)
        ))
    runner = TextTestRunner(verbosity = 2)
    return runner.run(suite)
