# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Liason tests
"""

from twisted.trial.unittest import TestCase
from twisted.internet import defer



from txopenid.consumer.liason import Liason



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
        return self.responses.pop(0)


    def post(self, *args, **kwargs):
        self.called.append(('post', args, kwargs))
        return self.responses.pop(0)



class LiasonTest(TestCase):


    def test_defaults(self):
        """
        By default, a L{Liason} uses in-memory storage devices.
        """
        l = Liason()
        self.assertTrue(isinstance(l.providers, l.providerStoreFactory))
        # XXX add HTTP agent
        # XXX add cryptographer/signer


    def test_init(self):
        """
        You can initialize a L{Liason} with some things.
        """
        agent = object()
        l = Liason(agent=agent)
        self.assertEqual(l.agent, agent)



