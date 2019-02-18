from dnstools.resolver import DnsResolver


INACTIVE_IP = '0.0.0.0'


def get_ipv4_address(domain):
    """Factory function to initialize IPAddress"""
    resolver = DnsResolver()
    domain_ips = resolver.query(domain, 'A')
    if len(domain_ips) > 0:
        ip_addr = domain_ips[0]
    else:
        ip_addr = INACTIVE_IP
    return IPAddress(ip_addr)


class IPAddress:
    def __init__(self, ipv4=INACTIVE_IP):
        self._ipv4 = ipv4

    def __repr__(self):
        return "IPAddress<ipv4='{}'>".format(self.ipv4)

    def __str__(self):
        return self.ipv4

    def __eq__(self, other):
        return self.ipv4 == other.ipv4

    @property
    def ipv4(self):
        """Return ipv4 address as a string"""
        return self._ipv4

    def online(self):
        """Return True if IP address is not inactive"""
        return self.ipv4 != INACTIVE_IP

    def reverse(self):
        """Reverse octets of ipv4 address, return as a string"""
        return '.'.join(reversed(self.ipv4.split('.')))
