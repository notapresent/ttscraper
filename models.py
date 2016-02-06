from google.appengine.ext import ndb


# class Torrent(ndb.Model):
#     """A main model for representing an individual Torrent entry."""
#     title = ndb.StringProperty(indexed=False)
#     btih = ndb.StringProperty(indexed=False)
#     dt = ndb.DateTimeProperty()
#     nb = ndb.IntegerProperty(indexed=False)
#     # descr = ndb.StringProperty(indexed=False)


class Account(ndb.Model):
    """Represents tracker user account along with its session"""
    username = ndb.StringProperty(indexed=False, required=True)
    password = ndb.StringProperty(indexed=False, required=True)
    userid = ndb.IntegerProperty(indexed=False, required=True)
    cookies = ndb.PickleProperty()

    @classmethod
    def get_one(cls):
        """Return one entry"""
        cls.query().get()
