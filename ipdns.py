#===================================================================================================
#   Module name:    ipdns.py
#   Author:         Zachary Colbert zcolbert1993@gmail.com
#   Date:           11-26-2017
#   Purpose:        Tools for resolving a domain name's IP address,
#                   and checking the domain or IP against an email blacklist.
#===================================================================================================
import dns.resolver


def reverse_ipv4(ip_address):
    return '.'.join(reversed(ip_address.split('.')))


class DnsResolver:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()

    def resolve_record(self, domain, record_type):
        try:
            answers = self.resolver.query(domain, record_type)
            return [rdata.to_text() for rdata in answers]
        except dns.resolver.NXDOMAIN:
            return list()

    def resolve_mx_from_domain(self, domain):
        return self.resolve_record(domain, 'MX')

    def resolve_ipv4_from_domain(self, domain):
        """Resolve domain name and return its IP address."""
        return self.resolve_record(domain, 'A')



def test():
    resolver = DnsResolver()
    print(resolver.resolve_record('google.com', 'A'))
    print(resolver.resolve_ipv4_from_domain('google.com'))
    print(resolver.resolve_ipv4_from_domain('realtorhouseportraits.com'))
    print(resolver.resolve_mx_from_domain('realtorhouseportraits.com'))


if __name__ == '__main__':
    test()
