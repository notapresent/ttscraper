"""All datastore models live in this module"""
import datetime
from contextlib import contextmanager

from google.appengine.ext import ndb


class Torrent(ndb.Model):
    """A main model for representing an individual Torrent entry."""
    title = ndb.StringProperty(indexed=False, required=True)
    btih = ndb.StringProperty(indexed=False, required=True)         # Infohash
    dt = ndb.DateTimeProperty(required=True)                        # Create/update time, as reported by tracker
    nbytes = ndb.IntegerProperty(indexed=False, required=True)      # Torrent data size, bytes

    @classmethod
    def get_latest_dt(cls):
        """Returns datetime for most recent torrent or start of epoch if no torrents"""
        latest_torrent = cls.query().order(-Torrent.dt).get()
        if latest_torrent:
            return latest_torrent.dt
        else:
            return datetime.datetime.utcfromtimestamp(0)

    @classmethod
    def save_torrent(cls, tid, title, btih, dt, nbytes):
        parent = Category.get_root_key()
        torrent = cls(id=tid, parent=parent, title=title, btih=btih, dt=dt, nbytes=nbytes)
        torrent.put()


class Account(ndb.Model):
    """Represents tracker user account along with its session"""
    username = ndb.StringProperty(indexed=False, required=True)
    password = ndb.StringProperty(indexed=False, required=True)
    userid = ndb.IntegerProperty(indexed=False, required=True)
    cookies = ndb.JsonProperty()

    @classmethod
    def get_one(cls):
        """Return one entry"""
        return cls.query().get()

    def __repr__(self):
        return "<Account username='{}' userid='{}' cookies=[{}]>".format(
            self.username, self.userid, self.cookies and self.cookies.keys())

    @classmethod
    @contextmanager
    def get_context(cls):
        """Provides account context and saves account if it was changed"""
        account = cls.get_one()
        values = account.to_dict()

        yield account

        if account.to_dict() != values:
            account.put()


class Category(ndb.Model):
    """Represents category entry"""
    title = ndb.StringProperty(indexed=False, required=True)
    num_torrents = ndb.IntegerProperty(indexed=True, required=True, default=0)
    is_leaf = ndb.BooleanProperty(indexed=True)
    last_changed = ndb.DateTimeProperty()

    @classmethod
    def get_root_key(cls):
        """Returns root category key for ancestor queries"""
        return ndb.Key(cls, 'r0')
