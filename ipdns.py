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
        pass

    def reverse_ip(self, ip_address):
        """Reverse the octets of an IP address."""
        return '.'.join(reversed(str(ip_address).split('.')))


class Domain:
    def __init__(self, domain_str):
        self.name = ''
        self.tld = ''
        self.split_domain(domain_str)

    def split_domain(self, domain):
        pass





class DomainValidator:
    def __init__(self, valid_tlds):
        self.resolver = DnsResolver()
        self.tld_validator = TLDValidator(valid_tlds)
        # Valid chars: a-z, A-Z, 0-9, -
        # Cannot begin or end with -
        # Cannot be numeric only
        self.valid_domain_char_regex = re.compile(
            '^[a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*[a-zA-Z0-9]$'
        )

    def domain_is_valid(self, domain):
        """Return True if domain is properly formatted,
        and contains a valid top level domain name."""
        return (self.tld_is_valid(domain.tld)
                and self.format_is_valid(domain.name))

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


class BlacklistChecker:

    def bl_lookup_by_ip(ip_address, blacklist):
        """Check ip_address against an IP blacklist.
        Query is in the form of: reversed_ip.target.blacklist.com"""
        return resolve_ip(reverse_ip(ip_address) + '.' + blacklist)


    def bl_lookup_by_domain(domain, blacklist):
        """Resolve IP from domain, then check against IP blacklist"""
        return bl_lookup_by_ip(resolve_ip(domain), blacklist)


    def dbl_lookup(target_domain, domain_blacklist):
        """Check target_domain against domain_blacklist.
        Query is in the form os: target_domain.domain_blacklist.com"""
        return resolve_ip(target_domain + '.' + domain_blacklist)
