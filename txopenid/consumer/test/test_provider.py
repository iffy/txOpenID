# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Provider storage tests
"""


from twisted.trial.unittest import TestCase
from twisted.internet import defer

from datetime import datetime


from txopenid.consumer.provider import (Provider, InMemoryProviderStore,
                                        Association)



class ProviderTest(TestCase):


    def test_attributes(self):
        """
        L{Provider} should have attributes known to a consumer
        """
        p = Provider('example.com')
        self.assertEqual(p.discovery_url, 'example.com')
        self.assertEqual(p.endpoint, None)



class ProviderStoreTestMixin:

    timeout = 1


    def getInstance(self):
        raise NotImplementedError("You must implement getInstance to use "
                                  "the ProviderStoreTestMixin")

    @defer.inlineCallbacks
    def test_add(self):
        """
        You can add L{Provider}s to a store
        """
        i = self.getInstance()
        
        provider = Provider('example.com')
        r = yield i.add('foo', provider)
        self.assertEqual(r, provider, "Should return the added Provider")


    @defer.inlineCallbacks
    def test_get(self):
        """
        You can get previously added L{Provider}s from the store.
        """
        i = self.getInstance()
        
        provider = Provider('example.com')
        yield i.add('foo', provider)
        r = yield i.get('foo')
        self.assertEqual(r, provider, "Should return an equal provider")


    def test_get_KeyError(self):
        """
        KeyError should be raised if the provider doesn't exist
        """
        i = self.getInstance()
        self.assertFailure(defer.maybeDeferred(i.get, 'foo'), KeyError)


    @defer.inlineCallbacks
    def test_keys_items_values(self):
        """
        You can get a list of all the provider names, name-value pairs or
        values stored in the store.
        """
        i = self.getInstance()
        
        keys = yield i.keys()
        self.assertEqual(list(keys), [])
        items = yield i.items()
        self.assertEqual(list(items), [])
        values = yield i.values()
        self.assertEqual(list(values), [])
        
        p1 = Provider('example.com')
        yield i.add('foo', p1)
        
        keys = yield i.keys()
        self.assertEqual(list(keys), ['foo'])
        items = yield i.items()
        self.assertEqual(list(items), [('foo', p1)])
        values = yield i.values()
        self.assertEqual(list(values), [p1])
        
        p2 = Provider('example2.com')
        yield i.add('bar', p2)
        
        keys = yield i.keys()
        self.assertEqual(set(keys), set(['foo', 'bar']))
        items = yield i.items()
        self.assertEqual(set(items), set([('foo', p1), ('bar', p2)]))
        values = yield i.values()
        self.assertEqual(set(values), set([p1, p2]))



class InMemoryProviderStoreTest(TestCase, ProviderStoreTestMixin):


    def getInstance(self):
        return InMemoryProviderStore()




class AssociationTest(TestCase):


    def test_attributes(self):
        """
        This should have all the attributes expected by the OpenID spec.
        """
        a = Association()
        self.assertEqual(a.expires_in, Association.expires_in)
        self.assertEqual(type(a.expires_in), int)
        self.assertNotEqual(a.created, None)
        self.assertTrue(a.created <= datetime.now())
        self.assertEqual(a.assoc_handle, None)
        self.assertEqual(a.mac_key, None)
        #XXX I know there are others.


    def test_init(self):
        """
        You can override all of the defaults on init
        """
        kwargs = {
            'expires_in': 245,
            'created': datetime(2000, 1, 1, 12, 45, 34),
            'assoc_handle': 'foobar',
            'mac_key': 'some key',
        }
        a = Association(**kwargs)
        self.assertEqual(a.expires_in, 245)
        self.assertEqual(a.created, datetime(2000, 1, 1, 12, 45, 34))
        self.assertEqual(a.assoc_handle, 'foobar')
        self.assertEqual(a.mac_key, 'some key')




