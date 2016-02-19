import webapp2
import webtest
import unittest
from mock import Mock, patch

from handlers import task_app


class Task_App_TestCase(unittest.TestCase):
   @patch('handlers.ObjectBuilder')
   def test_handler_response_status_is_200(self, ob):
       request = webapp2.Request.blank('/task/index')
       request.method = 'POST'

       response = request.get_response(task_app)

       self.assertEqual(response.status_int, 200)
