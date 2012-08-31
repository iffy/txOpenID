# txopenid
# Copyright (c) 2007 Phil Christensen
#
# See LICENSE for details

"""
Provider information and access
"""

from datetime import datetime



class Provider(object):
    """
    I am a collection of provider-specific data.
    
    @ivar discovery_url: URL to perform discovery on.
    
    @ivar endpoint: Endpoint URL
    """
    
    def __init__(self, discovery_url):
        self.discovery_url = discovery_url
        self.endpoint = None



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



class Association(object):
    """
    I am an association between an OpenID provider and consumer as seen by the
    consumer.
    """
    
    expires_in = 46800
    created = None
    assoc_handle = None
    mac_key = None
    
    
    def __init__(self, assoc_handle=None, mac_key=None, expires_in=None,
                 created=None):
        self.expires_in = expires_in or self.expires_in
        self.created = created or datetime.now()
        self.assoc_handle = assoc_handle
        self.mac_key = mac_key



