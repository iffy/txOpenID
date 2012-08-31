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



