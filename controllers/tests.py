import unittest
from controllers.vtestcontroller import VerbTestController


class TestVerbTestController(unittest.TestCase):

    def test_construction(self):
        ''' temporary test just to make sure that this all works'''
        controller = VerbTestController()
        self.assertIsNotNone(controller)


if __name__ == "__main__":
    unittest.main()
