import unittest
import logging

from google.appengine.ext import ndb
from google.appengine.ext.db import BadValueError
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from models import Account


class DatastoreTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()

        # Create a consistency policy that will simulate the High Replication
        # consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
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
    def setUp(self):
        super(AccountTestCase, self).setUp()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.userid = 123

    def test_account_is_stored(self):
        acc = Account(username=self.username, password=self.password, userid=self.userid)
        key = acc.put()
        stored = key.get()

        self.assertEqual(stored.username, self.username)
        self.assertEqual(stored.password, self.password)
        self.assertEqual(stored.userid, self.userid)

    def test_username_is_required(self):
        acc = Account(password=self.password, userid=self.userid)
        with self.assertRaises(BadValueError):
            acc.put()

    def test_password_is_required(self):
        acc = Account(username=self.username, userid=self.userid)
        with self.assertRaises(BadValueError):
            acc.put()

    def test_userid_is_required(self):
        acc = Account(password=self.password, username=self.username)
        with self.assertRaises(BadValueError):
            acc.put()

    def test_get_one_returns_entity(self):
        acc = Account(username=self.username, password=self.password, userid=self.userid)
        acc.put()

        result = Account.get_one()

        self.assertEqual(acc, result)
