from typing import Set

from dnstools.domain import Domain
from blacklist.blacklist import Blacklist


class DomainStatus:
    def __init__(self, domain: str):
        self._domain = Domain(domain)
        self.ip_listings = set()
        self.domain_listings = set()
        self.checked = False

    def __repr__(self):
        msg = "DomainStatus<domain='{}', status='{}'>"
        return msg.format(self.domain, self.status)

    @property
    def blacklists(self) -> Set[Blacklist]:
        return self.ip_listings.union(self.domain_listings)

    @property
    def domain(self) -> Domain:
        return self._domain

    @property
    def status(self) -> str:
        if not self.checked:
            return 'Unknown'
        if self.domain_is_listed() or self.ip_is_listed():
            return 'Listed'
        return 'Clean'

    def domain_is_listed(self) -> bool:
        return len(self.domain_listings) > 0

    def ip_is_listed(self) -> bool:
        return len(self.ip_listings) > 0

    def add_blacklist(self, blacklist: Blacklist):
        if blacklist.query_type == 'IP Address':
            self.ip_listings.add(blacklist)
        elif blacklist.query_type == 'Domain':
            self.domain_listings.add(blacklist)
        else:
            msg = 'Unknown blacklist type: {}'
            raise ValueError(msg.format(blacklist.query_type))
        self.checked = True
