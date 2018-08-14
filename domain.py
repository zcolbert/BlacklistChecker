from ipdns import DnsResolver
from socket import gaierror

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

    def is_active(self):
        try:
            self.get_ipv4()
            return True
        except gaierror:
            return False

