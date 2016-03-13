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
        parent = Category.get_root_key()    # TODO
        torrent = cls(id=tid, parent=parent, title=title, btih=btih, dt=dt, nbytes=nbytes)
        torrent.put()

    @classmethod
    def save_from_dict(cls, d):
        tid = int(d['tid'])
        title = d['title']
        btih = d['btih']
        dt = datetime.datetime.utcfromtimestamp(int(d['timestamp']))
        nbytes = int(d['nbytes'])
        # TODO description
        cls.save_torrent(tid, title, btih, dt, nbytes)

    @classmethod
    def get_latest_for_category(cls, cat, num_items):
        """Returns last num_items torrent in specified category and/or its subcategories"""
        return cls.query(ancestor=cat.key).order(-cls.dt).fetch(num_items)


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

    @classmethod
    def get_changed(cls):
        return [cls.get_root_key().get()]  # TODO
