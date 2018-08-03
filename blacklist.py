from abc import ABC, abstractmethod
from ipdns import DnsResolver
from socket import gaierror

class ListedDomain:
    def __init__(self, domain):
        self.domain = domain
        self.blacklists = []


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

    def lookup(self, domain):
        reversed_ip = domain.get_reverse_ipv4_address()
        lookup_addr = reversed_ip + '.' + self.query_zone
        return self.resolver.resolve_ipv4_from_domain(lookup_addr)


class DomainBlacklist(Blacklist):
    def __init__(self, query_zone):
        Blacklist.__init__(self, query_zone)
        self.query_type = 'domain'

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
            return True
        return False

    def check_against_all_blacklists(self, domain):
        for b in self.blacklists:
            result = self.check_against_blacklist(domain, b)
            print(result)

    def check_against_ip_blacklists(self, domain):
        for b in self.blacklists:
            if b.query_type == 'ip':
                result = self.check_against_blacklist(domain, b)
                print(result)

    def check_against_domain_blacklists(self, domain):
        for b in self.blacklists:
            if b.query_type == 'domain':
                result = self.check_against_blacklist(domain, b)
                print(result)

    def update_listed_domains(self, domain, blacklist):
        print('Updating blacklists')
        result = self.listed_domains[domain.name]
        print(result)

    def add_listing_if_nonexistent(self):
        pass

    def get_listing_info(self, domain):
        pass
