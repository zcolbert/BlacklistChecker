
class DomainRecord:
    def __init__(self, file_record=None):
        self.record = file_record
        self.name = ""
        self.role = ""
        self.master = ""
        self.account = ""
        self.acct_id = ""
        self.prev_listed = ""
        self.update_record()

    def update_record(self):
        if not self.record == None:
            self.name = self.record["Domain"]
            self.role = self.record["Role"]
            self.master = self.record["Master"]
            self.account = self.record["IBW Account Name"]
            self.acct_id = self.record["IBW Account ID"]


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






