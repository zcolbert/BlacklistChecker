import dnstools


class Domain:
    INACTIVE = 'Inactive'
    DEFAULT_IP = '0.0.0.0'

    def __init__(self, name):
        self._name = name
        self._ipv4 = Domain.DEFAULT_IP

    def __repr__(self):
        return f"Domain<hostname='{self.hostname}'>"

    def __str__(self):
        return self.hostname

    @property
    def hostname(self):
        """Return the domain name"""
        return self._name

    @property
    def tld(self):
        """Return the top level domain name"""
        return self.hostname.split('.')[-1]

    @property
    def ipv4_address(self, refresh=False):
        """Return ipv4 address"""
        if self._ipv4 == Domain.DEFAULT_IP or refresh is True:
            # query domain to get refreshed IPAddress
            try:
                self._ipv4 = dnstools.query_ipv4_from_host(self.hostname)
            except dnstools.HostError:
                self._ipv4 = Domain.INACTIVE
        return self._ipv4
