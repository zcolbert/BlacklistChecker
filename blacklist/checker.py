import logging

from typing import Sequence

from blacklist.blacklist import Blacklist, BlacklistType
from blacklist.status import DomainStatus


class BlacklistChecker:
    def __init__(self, blacklists: Sequence[Blacklist]):
        self.blacklists = {}
        self._init_blacklists(blacklists)

    def _init_blacklists(self, blacklists: Sequence[Blacklist]):
        for bl in blacklists:
            if not bl.query_type in self.blacklists:
                self.blacklists[bl.query_type] = set()
            self.blacklists[bl.query_type].add(bl)

    def query(self, hostname, type=BlacklistType.ALL):
        logging.info(f'Checking {hostname} ...')
        status = DomainStatus(hostname)
        if type == BlacklistType.ALL:
            self._query_all(status)
        else:
            self._query_lists(status, type)
        status.checked = True
        return status

    def _query_all(self, status):
        for bltype in self.blacklists.keys():
            self._query_lists(status, bltype)

    def _query_lists(self, status, type):
        blists = self.blacklists[type]
        for bl in blists:
            listed = bl.query(status.domain)
            if listed:
                (status.add_blacklist(bl))
