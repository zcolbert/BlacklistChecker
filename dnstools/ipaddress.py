from dnstools.resolver import DnsResolver


class IPv4Address:

    INACTIVE_IP = '0.0.0.0'

    def __init__(self, ipv4=INACTIVE_IP):
        self._ipv4 = ipv4

    def __repr__(self) -> str:
        return f"IPv4Address<ipv4='{self.ipv4}'>"

    def __str__(self) -> str:
        return self.ipv4

    def __eq__(self, other) -> bool:
        return self.ipv4 == other.ipv4

    @property
    def ipv4(self) -> str:
        """Return ipv4 address as a string"""
        return self._ipv4

    def is_active(self) -> bool:
        """Return True if IP address is not inactive"""
        return self.ipv4 != IPv4Address.INACTIVE_IP

    def reverse(self) -> str:
        """Reverse octets of ipv4 address, return as a string"""
        return '.'.join(reversed(self.ipv4.split('.')))


def get_ipv4_address(domain) -> IPv4Address:
    """Factory function to initialize IPAddress"""
    resolver = DnsResolver()
    domain_ips = resolver.query(domain, 'A')
    if len(domain_ips) > 0:
        ip_addr = domain_ips[0]
    else:
        ip_addr = IPv4Address.INACTIVE_IP
    return IPv4Address(ip_addr)
