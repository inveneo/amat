from amat.tests import *

class TestAuthController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='auth'))
        # Test response...
