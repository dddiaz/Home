import unittest
import home

class HomeTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        #self.app = home.test.test_client()

    def tearDown(self):
        pass

    #example test
    def test_equal_numbers(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()