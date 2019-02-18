import dns.resolver


class DnsResolver:
    def __init__(self):
        self._resolver = dns.resolver.Resolver()

    @property
    def norecord(self):
        return list()

    def query(self, domain_name, record_type):
        try:
            answers = self._resolver.query(domain_name, record_type)
            return [rdata.to_text() for rdata in answers]
        except dns.rdatatype.UnknownRdatatype:
            msg = "Invalid DNS record type: {}"
            raise ValueError(msg.format(record_type))
        except (dns.resolver.NXDOMAIN,
                dns.resolver.NoAnswer,
                dns.resolver.NoNameservers,
                dns.resolver.Timeout) as err:
            # lookup returned no result
            return self.norecord

