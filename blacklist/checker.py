from blacklist.blacklist import BlacklistType
from blacklist.status import DomainStatus


class BlacklistChecker:
    def __init__(self, blacklists):
        self.blacklists = {}
        self._init_blacklists(blacklists)

    def _init_blacklists(self, blacklists):
        for bl in blacklists:
            if not bl.query_type in self.blacklists:
                self.blacklists[bl.query_type] = set()
            self.blacklists[bl.query_type].add(bl)

    def query(self, domain, type=BlacklistType.ALL):
        status = DomainStatus(domain)
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
