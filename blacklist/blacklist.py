from enum import Enum
import dnstools
from dnstools.domain import Domain


class BlacklistType(Enum):
    """Enumeration of valid Blacklist types"""
    ALL = 'all'
    IP_ADDRESS = 'IP Address'
    DOMAIN = 'Domain'


class Blacklist:
    """Base class for Blacklists"""
    def __init__(self, query_zone: str, alias: str = ''):
        self._query_type = BlacklistType
        self._query_zone = query_zone
        self.alias = alias

    @property
    def query_type(self) -> BlacklistType:
        return self._query_type.value

    @property
    def query_zone(self) -> str:
        return self._query_zone

    def _get_lookup_string(self, domain) -> str:
        """Return a string used to query the blacklist"""
        pass

    def query(self, domain: Domain):
        lookup_addr = self._get_lookup_string(domain)
        result = dnstools.query(lookup_addr, 'A')
        return result != []


class IPBlacklist(Blacklist):
    """Represents an IP Blacklist"""
    def __init__(self, query_zone: str, alias: str = ''):
        super().__init__(query_zone, alias)
        self._query_type = BlacklistType.IP_ADDRESS

    def __repr__(self):
        return f"IPBlacklist<alias='{self.alias}', query_zone='{self.query_zone}'>"

    def _get_lookup_string(self, domain: Domain) -> str:
        reversed_ip = dnstools.reverse_ipv4_octets(domain.ipv4_address)
        return f'{reversed_ip}.{self.query_zone}'


class DomainBlacklist(Blacklist):
    """Represents a Domain Blacklist"""
    def __init__(self, query_zone: str, alias: str = ''):
        super().__init__(query_zone, alias)
        self._query_type = BlacklistType.DOMAIN

    def __repr__(self) -> str:
        return f"DomainBlacklist<alias='{self.alias}', query_zone='{self.query_zone}'>"

    def _get_lookup_string(self, domain: Domain):
        return f'{domain.hostname}.{self.query_zone}'


def create_blacklist(bltype: BlacklistType, qzone: str, alias: str) -> Blacklist:
    """Factory function to initialize Blacklists"""
    if bltype == BlacklistType.IP_ADDRESS.value:
        return IPBlacklist(qzone, alias)
    elif bltype == BlacklistType.DOMAIN.value:
        return DomainBlacklist(qzone, alias)
    else:
        msg = "Unknown Blacklist type: '{}'"
        raise ValueError(msg.format(bltype))
