from abc import ABC, abstractmethod
from ipdns import DnsResolver
from socket import gaierror
from domain import Domain



class ListedDomain(Domain):
    def __init__(self, domain_str):
        Domain.__init__(self, domain_str)
        self.blacklists = []
        self.domain_listings = 0
        self.ip_listings = 0

    def __repr__(self):
        return ('ListedDomain<name="%s" listings=%d>'
                % (self.name, len(self.blacklists)))

    def add_blacklist(self, blacklist):
        self.update_listings(blacklist)
        if blacklist not in self.blacklists:
            self.blacklists.append(blacklist)

    def update_listings(self, blacklist):
        if blacklist.query_type == 'IP Address':
            self.ip_listings += 1
        elif blacklist.query_type == 'Domain':
            self.domain_listings += 1

    def ip_is_listed(self):
        return self.ip_listings > 0

    def domain_is_listed(self):
        return self.domain_listings > 0


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
    def lookup(self, domain):
        pass


class IPBlacklist(Blacklist):
    def __init__(self, query_zone, alias=''):
        Blacklist.__init__(self, query_zone, alias)
        self.query_type = 'IP Address'

    def __repr__(self):
        return ('IPBlacklist<alias="%s" query_zone="%s">'
                 % (self.alias, self.query_zone))

    def lookup(self, domain):
        reversed_ip = domain.get_reverse_ipv4()
        lookup_addr = reversed_ip + '.' + self.query_zone
        try:
            return self.resolver.resolve_ipv4_from_domain(lookup_addr)
        except gaierror:
            return False


class DomainBlacklist(Blacklist):
    def __init__(self, query_zone, alias=''):
        Blacklist.__init__(self, query_zone, alias)
        self.query_type = 'Domain'

    def __repr__(self):
        return ('DomainBlacklist<alias="%s" query_zone="%s">'
               % (self.alias, self.query_zone))

    def lookup(self, domain):
        lookup_addr = domain.name + '.' + self.query_zone
        try:
            return self.resolver.resolve_ipv4_from_domain(lookup_addr)
        except gaierror:
            return False


class BlacklistChecker:
    def __init__(self, blacklists):
        self.resolver = DnsResolver()
        self.blacklists = blacklists
        self.listed_domains = {}

    def check_against_blacklist(self, domain, blacklist):
        result = blacklist.lookup(domain)
        if result:
            self.update_listed_domains(domain, blacklist)

    def check_against_all_blacklists(self, domain):
        for b in self.blacklists:
            self.check_against_blacklist(domain, b)

    def check_against_ip_blacklists(self, domain):
        for b in self.blacklists:
            if b.query_type == 'IP Address':
                self.check_against_blacklist(domain, b)

    def check_against_domain_blacklists(self, domain):
        for b in self.blacklists:
            if b.query_type == 'Domain':
                self.check_against_blacklist(domain, b)

    def update_listed_domains(self, domain, blacklist):
        if domain.name in self.listed_domains:
            self.listed_domains[domain.name].add_blacklist(blacklist)
        else:
            listing = ListedDomain(domain.name)
            listing.add_blacklist(blacklist)
            self.listed_domains[domain.name] = listing

    def domain_is_listed(self, domain):
        return domain.name in self.listed_domains

    def get_listing_info(self, domain):
        return self.listed_domains[domain.name].blacklists

    def get_listed_domains(self):
        return [self.listed_domains[d] for d in self.listed_domains]
