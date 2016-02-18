"""Static data storage"""


class BaseStaticStorage(object):
    """Base class for storage adapters. All subclasses must implement put and url_for_path methods"""
    def put(self, path, content):
        """Put object into storage at specified path"""
        raise NotImplementedError()

    def url_for_path(self, path):
        """Get absolute url for object stored at path"""
        raise NotImplementedError()
