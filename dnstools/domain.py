from dnstools.ipaddress import get_ipv4_address


class Domain:
    def __init__(self, name):
        self._name = name
        self._ipv4 = None

    def __repr__(self):
        return "Domain<name='{}'>".format(self.name)

    def __str__(self):
        return self.name

    @property
    def name(self):
        """Return the domain name"""
        return self._name

    @property
    def tld(self):
        """Return the top level domain name"""
        return self.name.split('.')[-1]

    @property
    def ipv4_address(self, refresh=False):
        """Return ipv4 address"""
        if self._ipv4 is None or refresh == True:
            # query domain to get refreshed IPAddress
            self._ipv4 = get_ipv4_address(self.name)
        return self._ipv4

    def is_active(self):
        return self.ipv4_address.is_active()
