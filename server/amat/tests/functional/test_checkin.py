from amat.tests import *

class TestCheckinController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='checkin'))
        # Test response...
