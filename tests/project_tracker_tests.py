from flask import Flask
from project_tracker import app
from project_tracker.models import User, Project, Note
from flask_mongoengine import MongoEngine
import unittest


app.config.from_object('config.TestingConfig')


class ProjectTrackerTestCase(unittest.TestCase):

    #set up DB
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        db = MongoEngine(app)
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client(self)



    def tearDown(self):
        pass

    def test_index(self): 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #Ensure Page Loads Correctly
    def test_index_returns_list(self): 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Track It!' in response.data)

    #Ensure user is redirected to login if they are not autneticated
    def test_login_redirect(self): 
        tester = app.test_client(self)
        response = tester.get('/create', content_type='html/text')
        self.assertTrue(response.status_code in range(300,399))

    #Ensure Login works correctly
    def test_login(self): 
        unitTester = User(username='UnitTester',password='password', email='unit@test.com')
        unitTester.save()
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = dict(inputEmail='UnitTester', inputPassword='password',login_form="login_form"),
            follow_redirects=True
            )
        self.assertTrue(unitTester.is_authenticated)
        unitTester.delete()

    #Ensure Post works correctly
    def test_project_create_route(self): 
        unitTester = User(username='UnitTester',password='password', email='unit@test.com')
        unitTester.is_authenticated = True
        unitTester.save()
        tester = app.test_client(self)
        response = tester.post(
            '/create',
            data = dict(title='TestTitle', public=True,description='TEST Description', form="form" ),
            follow_redirects=True
            )
        self.assertTrue(response.status_code in range(200,299))

        unitTester.delete()






if __name__ == '__main__':
    unittest.main()

