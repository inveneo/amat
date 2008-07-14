from amat.tests import *

class TestRegController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='reg'))
        # Test response...
