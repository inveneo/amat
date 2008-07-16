from amat.tests import *

class TestDumpController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='dump'))
        # Test response...
