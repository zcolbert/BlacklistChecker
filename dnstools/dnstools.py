from typing import List

import dns.resolver
import socket


class HostError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class EmptyHostError(HostError):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


def query(domain_name: str, record_type: str) -> List[str]:
    try:
        resolver = dns.resolver.Resolver()
        answers = resolver.query(domain_name, record_type)
        return [rdata.to_text() for rdata in answers]
    except dns.rdatatype.UnknownRdatatype:
        msg = "Invalid DNS record type: {}"
        raise ValueError(msg.format(record_type))
    except (dns.resolver.NXDOMAIN,
            dns.resolver.NoAnswer,
            dns.resolver.NoNameservers,
            dns.resolver.Timeout) as err:
        # lookup returned no result
        return list()


def query_ipv4_from_host(hostname: str) -> str:
    if hostname == '':
        raise EmptyHostError()
    result = query(hostname, record_type='a')
    if len(result) > 0:
        return result[0]
    raise HostError(f"Hostname {hostname} is offline or does not exist")


def host_is_active(hostname: str) -> bool:
    try:
        query_ipv4_from_host(hostname)
        return True
    except HostError:
        return False


def ip_is_active(ip_address: str) -> bool:
    try:
        socket.gethostbyaddr(ip_address)
        return True
    except socket.herror as err:
        return False


def reverse_ipv4_octets(ipv4: str) -> str:
    """Reverse octets of ipv4 address, return as a string"""
    return '.'.join(reversed(ipv4.split('.')))
