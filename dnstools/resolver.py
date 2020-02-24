from typing import List
import dns.resolver
import socket


class DnsResolver:
    def __init__(self):
        self._resolver = dns.resolver.Resolver()

    @property
    def norecord(self):
        return list()

    def query(self, domain_name: str, record_type: str) -> List[str]:
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

    def query_ipv4_from_domain(self, domain: str) -> List[str]:
        return self.query(domain, record_type='a')

    def ip_is_active(self, ip_address) -> bool:
        try:
            socket.gethostbyaddr(ip_address)
            return True
        except socket.herror as err:
            return False

    def host_is_active(self, hostname: str) -> bool:
        return self.query_ipv4_from_domain(hostname) != list()

