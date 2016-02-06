import unittest
import logging

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from google.appengine.ext import testbed

from models import Account


class DatastoreTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        ndb.get_context().clear_cache()

        self._logger = logging.getLogger()
        self._old_logging_level = self._logger.getEffectiveLevel()
        self._logger.setLevel(logging.ERROR)

    def tearDown(self):
        self.testbed.deactivate()
        self._logger.setLevel(self._old_logging_level)


class AccountTestCase(DatastoreTestCase):
    def test_account_is_stored(self):
        username = 'testuser'
        password = 'testpassword'
        userid = 12345

        acc = Account(username=username, password=password, userid=userid)
        key = acc.put()
        stored = key.get()

        self.assertEqual(stored.username, username)
        self.assertEqual(stored.password, password)
        self.assertEqual(stored.userid, userid)

    def test_username_is_required(self):
        acc = Account(password='abc123', userid=123)
        with self.assertRaises(BadValueError):
            acc.put()

    def test_password_is_required(self):
        acc = Account(username='abc123', userid=123)
        with self.assertRaises(BadValueError):
            acc.put()

    def test_userid_is_required(self):
        acc = Account(password='abc123', username='abc123')
        with self.assertRaises(BadValueError):
            acc.put()
