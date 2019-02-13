from abc import ABC, abstractmethod
from ipdns import DnsResolver
from domain import DomainStatus


class Blacklist(ABC):
    def __init__(self, query_zone, alias=''):
        self.resolver = DnsResolver()
        self.query_zone = query_zone
        self.query_type = ''
        self.alias = alias
        self.description = ''
        self.delisting = ''
        self.return_codes = {}

    @abstractmethod
    def query(self, domain):
        pass


class IPBlacklist(Blacklist):
    def __init__(self, query_zone, alias=''):
        Blacklist.__init__(self, query_zone, alias)
        self.query_type = 'IP Address'

    def __repr__(self):
        msg = "IPBlacklist<alias='{alias}' query_zone='{zone}'>"
        return msg.format(alias=self.alias, zone=self.query_zone)

    def query(self, domain):
        reversed_ip = domain.ipv4_address.reverse()
        lookup_addr = '{ip}.{zone}'.format(
            ip=reversed_ip,
            zone=self.query_zone)
        result = self.resolver.query(lookup_addr, 'A')
        return result != self.resolver.norecord


class DomainBlacklist(Blacklist):
    def __init__(self, query_zone, alias=''):
        Blacklist.__init__(self, query_zone, alias)
        self.query_type = 'Domain'

    def __repr__(self):
        msg = "DomainBlacklist<alias='{alias}' query_zone='{zone}'>"
        return msg.format(alias=self.alias, zone=self.query_zone)

    def query(self, domain):
        lookup_addr = domain.name + '.' + self.query_zone
        result = self.resolver.query(lookup_addr, 'A')
        return result != self.resolver.norecord


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


