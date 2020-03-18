import logging

from typing import Dict, List, Sequence

from blacklist.blacklist import Blacklist
from blacklist.status import DomainStatus

from dnstools import DnsResolver
from dnstools.domain import Domain


class BlacklistChecker:
    def __init__(self, blacklists: Sequence[Blacklist], resolver: DnsResolver):
        self.blacklists = blacklists
        self.blacklist_nameservers : Dict[str, List[str]] = {}
        self.resolver = resolver
        #self._init_blacklists(blacklists)

    def _init_blacklists(self, blacklists: Sequence[Blacklist]):
        for bl in blacklists:
            # resolve list of authoritative nameservers for each blacklist
            nameservers = self.resolver.query_ns_records(bl.query_zone)
            if nameservers != list():
                self.blacklist_nameservers[bl.query_zone] = nameservers

    def query(self, hostname: str):
        logging.info(f'Checking {hostname} ...')
        domain = Domain(hostname)
        lookup_status = DomainStatus(domain)

        for bl in self.blacklists:

            # query the formatted lookup string against blacklist
            lookup_addr = bl.get_lookup_string(domain)
            result = self.resolver.query_a_records(lookup_addr)

            listed = False
            if len(result) != 0:
                listed = True

            # record listing status for this blacklist
            lookup_status.add_blacklist(bl, listed)

        return lookup_status
