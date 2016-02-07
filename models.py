from google.appengine.ext import ndb


class Account(ndb.Model):
    """Represents tracker user account along with its session"""
    username = ndb.StringProperty(indexed=False, required=True)
    password = ndb.StringProperty(indexed=False, required=True)
    userid = ndb.IntegerProperty(indexed=False, required=True)
    cookies = ndb.PickleProperty()

    @classmethod
    def get_one(cls):
        """Return one entry"""
        return cls.query().get()
