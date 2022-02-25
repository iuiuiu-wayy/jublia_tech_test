import datetime
import json
try:
    from run import app
    import unittest
except Exception as e:
    print('Some modules are not loaded {}'.format(e))

class FlaskTest(unittest.TestCase):

    # check for success case
    def test_success(self):
        tester = app.test_client(self)
        url = '/save_emails'
        request_data = {
            'email_subject': 'test_subject',
            'email_content': 'this is some content here',
            'timestamp': '2022-02-25 10:40:00'
        }
        response = tester.post(url, data=request_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(),b'Task submitted' )
        self.assertEqual(response.content_type, "application/json")


    ### check for fail case
    def test_fail(self):
        tester = app.test_client(self)
        url = '/save_emails'
        request_data = {
            'email_subject': 'test_subject',
            'email_content': 'this is some content here',
        }
        response = tester.post(url, data=request_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(),b'Bad request' )
        self.assertEqual(response.content_type, "application/json")

    ### check different timestamp format
    def test_wrong_format(self):
        tester = app.test_client(self)
        url = '/save_emails'
        request_data = {
            'email_subject': 'test_subject',
            'email_content': 'this is some content here',
            'timestamp': '15 Dec 2015 23:12'
        }
        response = tester.post(url, data=request_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(),b'Bad timestamp format, should be YYYY-MM-MM HH:MM:SS' )
        self.assertEqual(response.content_type, "application/json")

     ### check for special characters
    def test_special_char_inputs(self):
        tester = app.test_client(self)
        url = '/save_emails'
        request_data = {
            'email_subject': 'test_subject',
            'email_content': '123234:"{!#$87@(%!@#$)_(*tent here',
            'timestamp': '2022-02-25 10:40:00'
        }
        response = tester.post(url, data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(),b'Task submitted' )
        self.assertEqual(response.content_type, "application/json")
if __name__ == "__main__":
    unittest.main()