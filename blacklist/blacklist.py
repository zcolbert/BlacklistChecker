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
        self.blacklists = blacklists

    def query(self, domain):
        status = DomainStatus(domain)
        for bl in self.blacklists:
            listed = bl.query(domain)
            if listed:
                status.add_blacklist(bl)
        return status

