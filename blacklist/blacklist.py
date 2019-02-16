from enum import Enum

from ipdns import DnsResolver


class BlacklistType(Enum):
    ALL = 'all'
    IP_ADDRESS = 'IP Address'
    DOMAIN = 'Domain'


def create_blacklist(bltype, qzone, alias):
    """Factory function to initialize Blacklists"""
    types = {
        BlacklistType.IP_ADDRESS.value: BlacklistType.IP_ADDRESS,
        BlacklistType.DOMAIN.value: BlacklistType.DOMAIN
    }
    return Blacklist(types[bltype], qzone, alias)


class Blacklist:
    def __init__(self, query_type, query_zone, alias=''):
        self._query_type = query_type
        self._query_zone = query_zone
        self.alias = alias
        self.resolver = DnsResolver()

    @property
    def query_type(self):
        return self._query_type.value

    @property
    def query_zone(self):
        return self._query_zone

    def __repr__(self):
        msg = "Blacklist<type='{}', alias='{}', query_zone='{}'>"
        return msg.format(self.query_type.value, self.alias, self.query_zone)

    def _get_lookup_string(self, domain):
        if self._query_type == BlacklistType.IP_ADDRESS:
            reversed_ip = domain.ipv4_address.reverse()
            return reversed_ip + '.' + self.query_zone
        elif self._query_type == BlacklistType.DOMAIN:
            return domain.name + '.' + self.query_zone
        else:
            msg = "Unknown blacklist type: '{}'"
            raise ValueError(msg.format(self.query_type))

    def query(self, domain):
        lookup_addr = self._get_lookup_string(domain)
        result = self.resolver.query(lookup_addr, 'A')
        return result != self.resolver.norecord

