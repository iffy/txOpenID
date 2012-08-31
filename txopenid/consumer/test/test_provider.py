# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Provider storage tests
"""


from twisted.trial.unittest import TestCase
from twisted.internet import defer, task

from datetime import datetime


from txopenid.consumer.provider import (Provider, InMemoryProviderStore,
                                        Association, InMemoryAssociationStore)


class FakeHTTPResponse:


    def __init__(self, text, headers=None, code=200):
        self.text = text
        self.headers = headers or {}
        self.code = code



class FakeHTTPAgent:


    def __init__(self, responses=None):
        self.responses = responses or []
        self.called = []


    def get(self, *args, **kwargs):
        self.called.append(('get', args, kwargs))
        return defer.succeed(self.responses.pop(0))


    def post(self, *args, **kwargs):
        self.called.append(('post', args, kwargs))
        return defer.succeed(self.responses.pop(0))



class ProviderTest(TestCase):


    def test_attributes(self):
        """
        L{Provider} should have attributes known to a consumer
        """
        p = Provider('example.com', agent='foo')
        self.assertEqual(p.discovery_url, 'example.com')
        self.assertEqual(p.endpoint, None)
        self.assertTrue(isinstance(p.associations,
                                   Provider.associationStoreFactory),
                        "Should have an association store created from the "
                        "associationStoreFactory")
        self.assertEqual(p.agent, 'foo')


    @defer.inlineCallbacks
    def test_discover(self):
        """
        Doing discovery will use the agent by default, then cache the url for
        later discovery attempts.
        """
        agent = FakeHTTPAgent([
            FakeHTTPResponse('stuff<URI>foobar</URI>morestuff'),
        ])
        
        p = Provider('example.com', agent=agent)
        url = yield p.discover()
        self.assertEqual(url, 'foobar')
        self.assertEqual(p.endpoint, 'foobar', "Set the endpoint")
        self.assertEqual(agent.called, [
            ('get', ('example.com',), {})
        ])
        
        # reset agent mock
        agent.called.pop()
        
        url2 = yield p.discover()
        self.assertEqual(url2, 'foobar')
        self.assertEqual(len(agent.called), 0, "Should not have used the http "
                         "agent because the value is cached")



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
        self.assertEqual(a.assoc_handle, None)
        self.assertEqual(a.mac_key, None)
        #XXX I know there are others.


    def test_init(self):
        """
        You can override all of the defaults on init
        """
        kwargs = {
            'assoc_handle': 'foobar',
            'mac_key': 'some key',
        }
        a = Association(**kwargs)
        self.assertEqual(a.assoc_handle, 'foobar')
        self.assertEqual(a.mac_key, 'some key')



class AssociationStoreTestMixin:

    timeout = 1
    

    def getIAssociationStore(self):
        raise NotImplementedError("Must implement getIAssociationStore")


    def fakePassageOfTime(self, seconds):
        """
        Make the store returned by L{getIAssociationStore} think that a number
        of seconds has elapsed.
        """
        raise NotImplementedError("You must implement fakePassageOfTime")


    @defer.inlineCallbacks
    def test_add(self):
        """
        You can add associations
        """
        store = self.getIAssociationStore()
        
        a = Association(assoc_handle='foo')
        b = yield store.add(a)
        self.assertEqual(b, 'foo', "Should return the assoc_handle")


    @defer.inlineCallbacks
    def test_get(self):
        """
        You can get associations by the handle
        """
        store = self.getIAssociationStore()
        
        a = Association(assoc_handle='foo')
        b = yield store.add(a)
        c = yield store.get(b)
        self.assertEqual(c, a, "Should return an equivalent Association")


    @defer.inlineCallbacks
    def test_get_expired(self):
        """
        You can't get expired associations out.
        """
        store = self.getIAssociationStore()
        
        a = Association(assoc_handle='foo')
        b = yield store.add(a, expires_in=100)
        self.fakePassageOfTime(101)
        self.assertFailure(defer.maybeDeferred(store.get, b), KeyError,
                           "When an association expires, it should be gone")




class InMemoryAssociationStoreTest(TestCase, AssociationStoreTestMixin):

    
    def getIAssociationStore(self):
        self._reactor = task.Clock()
        return InMemoryAssociationStore(reactor=self._reactor)


    def fakePassageOfTime(self, seconds):
        self._reactor.advance(seconds)



