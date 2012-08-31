# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Liason for the consumer to some providers
"""


from txopenid.consumer.provider import InMemoryProviderStore



class Liason(object):
    """
    I am used on the consumer side to communicate with remote OpenID providers.
    
    @ivar agent: HTTP agent
    
    @ivar providers: A store of L{Provider}s.
    """
    
    
    providerStoreFactory = InMemoryProviderStore
    
    
    def __init__(self, agent=None):
        self.providers = self.providerStoreFactory()
        self.agent = agent



