#===================================================================================================
#   Module name:    ipdns.py
#   Author:         Zachary Colbert zcolbert1993@gmail.com
#   Date:           11-26-2017
#   Purpose:        Tools for resolving a domain name's IP address,
#                   and checking the domain or IP against an email blacklist.
#===================================================================================================
import socket
import re # regex for domain validation


class DnsResolver:
    def resolve_ipv4_from_domain(self, domain):
        """Resolve domain name and return its IP address."""
        return socket.gethostbyname(domain)

    def resolve_domain_from_ipv4(self, ip_address):
        raise NotImplementedError('DnsResolver.resolve_domain_from_ipv4 not implemented')


class Domain:
    def __init__(self, domain_str):
        self.resolver = DnsResolver()
        self.name = domain_str
        self.tld = self.name.split('.')[-1]

    def __repr__(self):
        return 'Domain<name="%s">' % self.name

    def get_ipv4(self):
        return self.resolver.resolve_ipv4_from_domain(self.name)

    def get_reverse_ipv4(self):
        """Reverse the octets of an IP address."""
        return '.'.join(reversed(self.get_ipv4().split('.')))


class DomainValidator:
    def __init__(self, valid_tlds):
        self.resolver = DnsResolver()
        self.tld_validator = TLDValidator(valid_tlds)
        self.valid_domain_char_regex = re.compile(
            # Valid chars: a-z, A-Z, 0-9, '-'
            # Cannot begin or end with '-', cannot be only numeric
            '^[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*[a-zA-Z0-9]$'
        )

    def domain_is_valid(self, domain_str):
        """Return True if domain is properly formatted,
        and contains a valid top level domain name."""
        domain = Domain(domain_str)
        return (self.tld_is_valid(domain.get_tld())
                and self.format_is_valid(domain.get_name()))

    def tld_is_valid(self, tld):
        return self.tld_validator.tld_is_valid(tld)

    def format_is_valid(self, domain):
        if len(domain) < 3 or len(domain) > 63:
            return False
        result = self.valid_domain_char_regex.search(domain)
        return result is not None

    def domain_is_active(self, domain):
        pass


class TLDValidator:
    def __init__(self, valid_tlds):
        self.valid_tlds = valid_tlds

    def tld_is_valid(self, tld):
        if tld == '':
            return False
        return tld.upper() in self.valid_tlds


