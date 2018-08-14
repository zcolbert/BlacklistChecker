#===================================================================================================
#   Module name:    ipdns.py
#   Author:         Zachary Colbert zcolbert1993@gmail.com
#   Date:           11-26-2017
#   Purpose:        Tools for resolving a domain name's IP address,
#                   and checking the domain or IP against an email blacklist.
#===================================================================================================
import socket


class DnsResolver:
    def resolve_ipv4_from_domain(self, domain):
        """Resolve domain name and return its IP address."""
        return socket.gethostbyname(domain)

    def resolve_domain_from_ipv4(self, ip_address):
        raise NotImplementedError('DnsResolver.resolve_domain_from_ipv4 not implemented')



