from project_tracker import app
import unittest


class FlaskTestCase(unittest.TestCase):
    #Ensure that flask was set up correctly
    def test_index(self): 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #Ensure Page Loads Correctly
    def test_index_returns_list(self): 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Track It!' in response.data)

    def test_project_create(self):
        #Build out here
        pass



if __name__ == '__main__':
    unittest.main()

