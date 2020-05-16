from app import app
import unittest

class FlaskTestCase(unittest.TestCase):
    #test flask server
    def test_index(self):
        tester = app.test_client()
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test correct load
    def test_login_page(self):
        tester = app.test_client()
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Igrachite Official' in response.data)    

    def test_succesful_login(self):
        tester = app.test_client()
        response = tester.post('/', data=dict(username='Random', password='Ivanov'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_unsuccesful_login(self):
        tester = app.test_client()
        response = tester.post('/', data=dict(username='wrong', password='wrong'), follow_redirects=True)
        self.assertNotEqual(response.status_code, 200)

    def test_logout(self):
        tester = app.test_client()
        tester.post('/', data=dict(username='Phineas', password='club33'), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_send_message(self):
    #     tester = app.test_client()
    #     tester.post('/', data=dict(username='Random', password='Ivanov'), follow_redirects=True)
    #     response = tester.post('/chat', data=dict(user_message='angena'))
    #     self.assertFalse(b'angena' in response.data)
        
        



if __name__ == '__main__':
    unittest.main()