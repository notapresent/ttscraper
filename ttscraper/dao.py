"""Data access layer"""
import datetime
from contextlib import contextmanager

from google.appengine.ext import ndb

from models import Torrent, Category, Account


def latest_torrent_dt():
    """Returns datetime for most recent torrent or start of epoch if no torrents"""
    latest_torrent = Torrent.query().order(-Torrent.dt).get()
    if latest_torrent:
        return latest_torrent.dt
    else:
        return datetime.datetime.utcfromtimestamp(0)


def latest_torrents(num_items, cat_key=None):
    """Returns num_items torrent in specified category and/or its subcategories"""
    if cat_key is None:
        cat_key = root_category_key()

    return Torrent.query(ancestor=cat_key).order(-Torrent.dt).fetch(num_items)


def save_torrent(key, fields):
    """Save torrent, identified by key"""
    t = Torrent(key=key, **fields)
    t.put()


def torrent_key(categories, tid):
    """Make full key for torrent entry"""
    return ndb.Key(Category, 'r0', Torrent, tid)    # FIXME
    pairs = [(Category, '{}{}'.format(cat[1], cat[0])) for cat in categories]
    pairs.append((Torrent, tid))
    return ndb.Key(pairs=pairs)


def root_category_key():
    """Returns root category key"""
    return ndb.Key(Category, 'r0')


def changed_cat_keys(dt):
    """Returns keys for categories, changed after specified time"""
    return [root_category_key()]  # TODO


def get_account():
    """Return one entry"""
    return Account.query().get()


@contextmanager
def account_context(acc=None):
    """Provides account context and saves account entry if it was changed"""
    account = acc or get_account()
    values = account.to_dict()

    yield account

    if account.to_dict() != values:
        account.put()

