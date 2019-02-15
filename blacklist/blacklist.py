from enum import Enum

from ipdns import DnsResolver
from domain import DomainStatus


class BlacklistType(Enum):
    IP_ADDRESS = "IP Address"
    DOMAIN = "Domain"


def create_blacklist(type, zone, alias):
    """Factory function to initialize Blacklists"""
    return Blacklist(type, zone, alias)


def get_lookup_string(bltype, domain, query_zone):
    if bltype == BlacklistType.IP_ADDRESS:
        reversed_ip = domain.ipv4_address.reverse()
        return reversed_ip + '.' + query_zone
    elif bltype == BlacklistType.DOMAIN:
        return domain.name + '.' + query_zone
    else:
        msg = "Unknown blacklist type: '{}'"
        raise ValueError(msg.format(bltype))


class BlacklistChecker:
    def __init__(self, blacklists):
        self.resolver = DnsResolver()
        self.blacklists = {}
        self._init_blacklists(blacklists)

    def _init_blacklists(self, blacklists):
        for bl in blacklists:
            if not bl.query_type in self.blacklists:
                self.blacklists[bl.query_type] = set()
            self.blacklists[bl.query_type].add(bl)

    def query(self, domain, type='all'):
        status = DomainStatus(domain)
        if (type=='all' or type=='domain'):
            self._query_domain_blacklists(status)
        # Check IP blacklists only if domain is active
        if (type == 'all' or type=='ip') and domain.is_active():
            self._query_ip_blacklists(status)
        return status

    def _query_ip_blacklists(self, status):
        for bl in self.blacklists['IP Address']:
            listed = bl.query(status.domain)
            if listed:
                status.add_blacklist(bl)

    def _query_domain_blacklists(self, status):
        for bl in self.blacklists['Domain']:
            listed = bl.query(status.domain)
            if listed:
                status.add_blacklist(bl)


class Blacklist:
    def __init__(self, query_type, query_zone, alias=''):
        self.query_type = query_type
        self.query_zone = query_zone
        self.alias = alias
        self.resolver = DnsResolver()

    def __repr__(self):
        msg = "Blacklist<type='{}', alias='{}', query_zone='{}'>"
        return msg.format(self.query_type.value, self.alias, self.query_zone)

    def get_lookup_string(self, domain):
        if self.query_type == BlacklistType.IP_ADDRESS.value:
            reversed_ip = domain.ipv4_address.reverse()
            return reversed_ip + '.' + self.query_zone
        elif self.query_type == BlacklistType.DOMAIN.value:
            return domain.name + '.' + self.query_zone
        else:
            msg = "Unknown blacklist type: '{}'"
            raise ValueError(msg.format(self.query_type))

    def query(self, domain):
        lookup_addr = self.get_lookup_string(domain)
        result = self.resolver.query(lookup_addr, 'A')
        return result != self.resolver.norecord

