
class DomainRecord:
    def __init__(self):
        self.name = ""
        self.role = ""
        self.master = ""
        self.account = ""
        self.acct_id = ""
        self.prev_listed = ""

class ListedDomain(DomainRecord):
    """Represents a domain name that has been listed on an
    IP Address or Domain based email blacklist"""
    def __init__(self, parent, ip_address, list_name, list_type):
        DomainRecord.__init__(self)
        self.name = parent.name
        self.role = parent.role
        self.master = parent.master
        self.account = parent.account
        self.acct_id = parent.acct_id
        self.prev_listed = parent.prev_listed

        self.ip_address = ip_address
        self.list_name = list_name
        self.list_type = list_type






