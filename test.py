from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    #test flask server
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test correct load
    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Igrachite Official' in response.data)    

    def test_succesful_login(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username='Random', password='Ivanov'), follow_redirects=True)
        self.assertTrue(b'Random' in response.data)

    def test_unsuccesful_login(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(username='wrong', password='wrong'), follow_redirects=True)
        self.assertFalse(b'Logout' in response.data)



if __name__ == '__main__':
    unittest.main()