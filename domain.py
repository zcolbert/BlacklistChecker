from ipdns import DnsResolver, IPAddress


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
        return self._name

    @property
    def tld(self):
        return self.name.split('.')[-1]

    @property
    def ipv4_address(self, refresh=False):
        if self._ipv4 is None or refresh == True:
            # refresh ipv4 address value
            resolver = DnsResolver()
            ip_addrs = resolver.query(self.name, 'A')
            if len(ip_addrs) > 0:
                self._ipv4 = IPAddress(ip_addrs[0])
            else:
                self._ipv4 = IPAddress()
        return self._ipv4

    def is_active(self):
        return self.ipv4_address != IPAddress()


class DomainStatus:
    def __init__(self, domain, status='Online'):
        self._domain = domain
        self.status = status
        self.ip_listings = set()
        self.domain_listings = set()

    def __repr__(self):
        msg = "DomainStatus<domain='{}', status='{}'>"
        return msg.format(self.domain, self.status)

    @property
    def domain(self):
        return self._domain

    @property
    def blacklists(self):
        return self.ip_listings.union(self.domain_listings)

    def domain_is_listed(self):
        return len(self.domain_listings) > 0

    def ip_is_listed(self):
        return len(self.ip_listings) > 0

    def domain_is_online(self):
        return self.domain.is_active()

    def add_blacklist(self, blacklist):
        if blacklist.query_type == 'IP Address':
            self.ip_listings.add(blacklist)
        elif blacklist.query_type == 'Domain':
            self.domain_listings.add(blacklist)
        else:
            msg = 'Unknown blacklist type: {}'
            raise ValueError(msg.format(blacklist.query_type))
        self.status = 'Listed'


