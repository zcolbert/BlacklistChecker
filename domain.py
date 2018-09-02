from socket import gaierror
import re # regex for domain validation
import ipdns


class Domain:
    def __init__(self, domain_str):
        self.resolver = ipdns.DnsResolver()
        self.name = domain_str
        self.tld = self.name.split('.')[-1]

    def __repr__(self):
        return 'Domain<name="%s">' % self.name

    def get_ipv4(self):
        ip_addrs = self.resolver.resolve_ipv4_from_domain(self.name)
        return ip_addrs[0]

    def get_reverse_ipv4(self):
        """Reverse the octets of an IP address."""
        return ipdns.reverse_ipv4(self.get_ipv4())

    def is_active(self):
        return self.get_ipv4() != ''

    def has_mx_record(self):
        mx = self.resolver.resolve_mx_from_domain(self.name)
        return len(mx) > 0


class DomainValidator:
    def __init__(self, valid_tlds):
        self.resolver = ipdns.DnsResolver()
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
        return (self.tld_is_valid(domain.tld)
                and self.format_is_valid(domain.tld))

    def tld_is_valid(self, tld):
        return self.tld_validator.tld_is_valid(tld)

    def format_is_valid(self, domain):
        if len(domain) < 3 or len(domain) > 63:
            return False
        result = self.valid_domain_char_regex.search(domain)
        return result is not None


class TLDValidator:
    def __init__(self, valid_tlds):
        self.valid_tlds = valid_tlds

    def tld_is_valid(self, tld):
        if tld == '':
            return False
        return tld.upper() in self.valid_tlds

