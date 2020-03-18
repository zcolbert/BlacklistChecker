from dnstools.domain import Domain
from blacklist.blacklist import Blacklist, BlacklistType


class DomainStatus:

    UNKNOWN = 'Unknown'
    LISTED = 'Listed'
    CLEAN = 'Clean'

    def __init__(self, domain: Domain):
        self._domain = domain
        self.ip_listings = set()
        self.domain_listings = set()
        self.checked = False

    def __repr__(self):
        msg = "DomainStatus<domain='{}', status='{}'>"
        return msg.format(self.domain, self.status)

    @property
    def domain(self) -> Domain:
        return self._domain

    @property
    def status(self) -> str:
        if not self.checked:
            return DomainStatus.UNKNOWN
        if self.domain_is_listed() or self.ip_is_listed():
            return DomainStatus.LISTED
        return DomainStatus.CLEAN

    def domain_is_listed(self) -> bool:
        return len(self.domain_listings) > 0

    def ip_is_listed(self) -> bool:
        return len(self.ip_listings) > 0

    def add_blacklist(self, blacklist: Blacklist, listed: bool):
        if listed:
            if blacklist.query_type == BlacklistType.IP_ADDRESS.value:
                self.ip_listings.add(blacklist)
            else:
                self.domain_listings.add(blacklist)
        self.checked = True
