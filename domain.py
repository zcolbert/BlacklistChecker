from ipdns import DnsResolver, IPAddress


class Domain:
    def __init__(self, name):
        self._name = name

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
    def ipv4_address(self):
        resolver = DnsResolver()
        ip_addrs = resolver.query(self.name, 'A')
        if len(ip_addrs) > 0:
            return IPAddress(ip_addrs[0])
        else:
            return IPAddress()

    def is_active(self):
        return self.ipv4_address != IPAddress()


class DomainStatus:
    def __init__(self, domain):
        self.domain = domain
        self.status = ''
        self.ip_listings = set()
        self.domain_listings = set()

    def __repr__(self):
        msg = "DomainStatus<domain='{}', status='{}'"
        return msg.format(self.domain, self.status)

    def add_blacklist(self, blacklist):
        if blacklist.query_type == 'IP Address':
            self.ip_listings.add(blacklist)
        elif blacklist.query_type == 'Domain':
            self.domain_listings.add(blacklist)
        else:
            msg = 'Unknown blacklist type: {}'
            raise ValueError(msg.format(blacklist.query_type))
        self.status = 'Listed'

