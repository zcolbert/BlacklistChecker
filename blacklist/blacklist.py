from abc import ABC
from abc import abstractmethod
from enum import Enum

from dnstools.resolver import DnsResolver


class BlacklistType(Enum):
    """Enumeration of valid Blacklist types"""
    ALL = 'all'
    IP_ADDRESS = 'IP Address'
    DOMAIN = 'Domain'


def create_blacklist(bltype, qzone, alias):
    """Factory function to initialize Blacklists"""
    if bltype == BlacklistType.IP_ADDRESS.value:
        return IPBlacklist(qzone, alias)
    elif bltype == BlacklistType.DOMAIN.value:
        return DomainBlacklist(qzone, alias)
    else:
        msg = "Unknown Blacklist type: '{}'"
        raise ValueError(msg.format(bltype))


class Blacklist(ABC):
    """Abstract base class for Blacklists"""
    def __init__(self, query_zone, alias=''):
        self._query_type = BlacklistType
        self._query_zone = query_zone
        self.alias = alias
        self.resolver = DnsResolver()

    @property
    def query_type(self):
        return self._query_type.value

    @property
    def query_zone(self):
        return self._query_zone

    @abstractmethod
    def _get_lookup_string(self, domain):
        """Return a string used to query the blacklist"""
        pass

    def query(self, domain):
        lookup_addr = self._get_lookup_string(domain)
        result = self.resolver.query(lookup_addr, 'A')
        return result != self.resolver.norecord


class IPBlacklist(Blacklist):
    """Represents an IP Blacklist"""
    def __init__(self, query_zone, alias=''):
        Blacklist.__init__(self, query_zone, alias)
        self._query_type = BlacklistType.IP_ADDRESS

    def __repr__(self):
        msg = "IPBlacklist<alias='{}', query_zone='{}'>"
        return msg.format(self.alias, self.query_zone)

    def _get_lookup_string(self, domain):
        reversed_ip = domain.ipv4_address.reverse()
        return reversed_ip + '.' + self.query_zone


class DomainBlacklist(Blacklist):
    """Represents a Domain Blacklist"""
    def __init__(self, query_zone, alias=''):
        Blacklist.__init__(self, query_zone, alias)
        self._query_type = BlacklistType.DOMAIN

    def __repr__(self):
        msg = "DomainBlacklist<alias='{}', query_zone='{}'>"
        return msg.format(self.alias, self.query_zone)

    def _get_lookup_string(self, domain):
        return domain.name + '.' + self.query_zone
