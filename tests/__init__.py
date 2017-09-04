from tests.users_tests import UserManagerTests
from tests.locations_test import LocationManagerTests
from tests.chores_test import ChoresManagerTests
from tests.fulfillment_tests import FulfillmentManagerTests

from unittest import TestLoader, TextTestRunner, TestSuite

if __name__ == "__main__":
    run()

def run():
    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(UserManagerTests),
        loader.loadTestsFromTestCase(LocationManagerTests),
        loader.loadTestsFromTestCase(ChoresManagerTests),
        loader.loadTestsFromTestCase(FulfillmentManagerTests)
        ))
    runner = TextTestRunner(verbosity = 2)
    return runner.run(suite)
