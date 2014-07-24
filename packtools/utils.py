#coding: utf-8
import hmac
import types
import hashlib
import logging
import functools


logger = logging.getLogger(__name__)


def _feed_hash(message, hash):
    """
    Feeds `hash` with `message` in order to
    generate a digest.
    """
    if hasattr(message, 'read'):
        while True:
            chunk = message.read(1024)
            if not chunk:
                break
            hash.update(chunk)

    elif isinstance(message, types.StringType):
        hash.update(message)

    else:
        raise TypeError('Unsupported type %s' % type(message))


def authenticate_message(message, secret='sekretz'):
    """
    Returns a digest for the message based on the given secret

    ``message`` is the file object or byte string to be calculated
    ``secret`` is a shared key used by the hash algorithm
    """
    hash = hmac.new(secret, '', hashlib.sha1)
    _feed_hash(message, hash)

    return hash.hexdigest()


def checksum_file(filepath, callable):
    """
    Returns a digest for the filepath based on the given secret

    ``filepath`` is the file to have its bytes calculated
    ``secret`` is a shared key used by the hash algorithm
    """
    with open(filepath, 'rb') as f:
        hash = callable()
        _feed_hash(f, hash)

    return hash.hexdigest()


def setdefault(object, attribute, producer):
    """
    Like dict().setdefault but for object attributes.
    """
    if not hasattr(object, attribute):
        setattr(object, attribute, producer())

    return getattr(object, attribute)


def cachedmethod(wrappee):
    """Caches method calls within known arguments.
    """
    @functools.wraps(wrappee)
    def wrapper(self, *args, **kwargs):
        key = (args, tuple(kwargs.items()))
        cache_attrname = '__' + wrappee.__name__

        cache = setdefault(self, cache_attrname, lambda: {})
        if key not in cache:
            cache[key] = wrappee(self, *args, **kwargs)

        return cache[key]

    return wrapper

