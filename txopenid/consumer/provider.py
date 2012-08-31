# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Provider information and access
"""

from twisted.internet import reactor

from datetime import datetime



class Association(object):
    """
    I am an association between an OpenID provider and consumer as seen by the
    consumer.
    """

    assoc_handle = None
    mac_key = None
    
    
    def __init__(self, assoc_handle=None, mac_key=None):
        self.assoc_handle = assoc_handle
        self.mac_key = mac_key



class InMemoryAssociationStore(object):
    """
    I store L{Association}s by C{assoc_handle} for a time.
    """


    def __init__(self, reactor=reactor):
        self._associations = {}
        self.reactor = reactor


    def add(self, association, expires_in=None):
        """
        Add an association in memory.
        
        @param assocation: The association to store.  This must have an
            C{assoc_handle} attribute which will be used as the key to later
            L{get} the association back out.

        @param expires_in: Number of seconds after which the association will
            be removed from this store.

        @return: The C{association.assoc_handle}
        """
        self._associations[association.assoc_handle] = association
        if expires_in is not None:
            def rmAssoc(handle):
                del self._associations[handle]
            self.reactor.callLater(expires_in, rmAssoc, association.assoc_handle)
        return association.assoc_handle


    def get(self, handle):
        """
        Get a previously stored, unexpired association.
        
        @param handle: The C{assoc_handle} of the L{Association} you wish to
            find.
        
        @return: an L{Association}
        """
        return self._associations[handle]



class Provider(object):
    """
    I am a collection of provider-specific data.

    @var associationStoreFactory: Factory used to make my C{associations}.

    @ivar discovery_url: URL to perform discovery on.
    
    @ivar endpoint: Endpoint URL
    
    @ivar associations: A place to store and retrieve L{Association}s.
    """
    
    associationStoreFactory = InMemoryAssociationStore

    
    def __init__(self, discovery_url):
        self.discovery_url = discovery_url
        self.endpoint = None
        self.associations = self.associationStoreFactory()



class InMemoryProviderStore(object):
    """
    I hold L{Provider}s in memory.
    """
    
    
    def __init__(self):
        self.providers = {}
    
    
    def add(self, name, provider):
        """
        Store a L{Provider} under a C{name}.
        
        @param name: Name/key of provider.
        
        @type provider: L{Provider}
        
        @return: C{provider} passed in.
        """
        self.providers[name] = provider
        return provider


    def get(self, name):
        """
        Get a previously-stored L{Provider} by name/key.
        """
        return self.providers[name]


    def keys(self):
        """
        Get all the provider names/keys.
        
        @return: List of provider names.
        """
        return self.providers.keys()


    def items(self):
        return self.providers.items()


    def values(self):
        return self.providers.values()



