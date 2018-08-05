from abc import ABC, abstractmethod
from ipdns import DnsResolver

class ListedDomain:
    def __init__(self, domain):
        self.domain = domain
        self.blacklists = []

    def __repr__(self):
        return ('ListedDomain<name="%s" listings=%d>'
                % (self.domain.name, len(self.blacklists)))

    def add_blacklist(self, blacklist):
        if not blacklist in self.blacklists:
            self.blacklists.append(blacklist)


class Blacklist(ABC):
    def __init__(self, query_zone):
        self.resolver = DnsResolver()
        self.query_zone = query_zone
        self.query_type = ''
        self.alias = ''
        self.description = ''
        self.delisting = ''
        self.return_codes = {}

    @abstractmethod
    def lookup(self, domain):
        pass


class IPBlacklist(Blacklist):
    def __init__(self, query_zone):
        Blacklist.__init__(self, query_zone)
        self.query_type = 'ip'

    def __repr__(self):
        return 'IPBlacklist<query_zone="%s">' % self.query_zone

    def lookup(self, domain):
        reversed_ip = domain.get_reverse_ipv4()
        lookup_addr = reversed_ip + '.' + self.query_zone
        return self.resolver.resolve_ipv4_from_domain(lookup_addr)


class DomainBlacklist(Blacklist):
    def __init__(self, query_zone):
        Blacklist.__init__(self, query_zone)
        self.query_type = 'domain'

    def __repr__(self):
        return 'DomainBlacklist<query_zone="%s">' % self.query_zone

    def lookup(self, domain):
        lookup_addr = domain.name + '.' + self.query_zone
        return self.resolver.resolve_ipv4_from_domain(lookup_addr)


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
            if b.query_type == 'ip':
                self.check_against_blacklist(domain, b)

    def check_against_domain_blacklists(self, domain):
        for b in self.blacklists:
            if b.query_type == 'domain':
                self.check_against_blacklist(domain, b)

    def update_listed_domains(self, domain, blacklist):
        if domain.name in self.listed_domains:
            self.listed_domains[domain.name].add_blacklist(blacklist)
        else:
            listing = ListedDomain(domain)
            listing.add_blacklist(blacklist)
            self.listed_domains[domain.name] = listing

    def domain_is_listed(self, domain):
        return domain.name in self.listed_domains

    def get_listing_info(self, domain):
        return self.listed_domains[domain.name].blacklists

    def get_listed_domains(self):
        return [self.listed_domains[d] for d in self.listed_domains]
