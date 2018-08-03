#===================================================================================================
#   Module name:    ipdns.py
#   Author:         Zachary Colbert zcolbert1993@gmail.com
#   Date:           11-26-2017
#   Purpose:        Tools for resolving a domain name's IP address,
#                   and checking the domain or IP against an email blacklist.
#===================================================================================================
import socket


class DnsResolver:
    def __init__(self, valid_tlds):
        self.valid_tlds = valid_tlds

    def resolve_ip(self, domain):
        """Resolve domain name and return its IP address."""
        if not self.valid_domain(domain):
             raise ValueError("Invalid domain: " + domain)
        return socket.gethostbyname(domain)

    def reverse_ip(self, ip_address):
        """Reverse the octets of an IP address."""
        return '.'.join(reversed(str(ip_address).split('.')))

    def valid_tld(self, tld):
        return tld in self.valid_tlds

    def valid_domain(self, domain):
        pass



class Domain:
    def __init__(self, domain_name, ip_address):
        self.name = domain_name
        self.ip_address = ip_address


def valid_tld(tld):
    """Return True if tld is a valid top level domain"""
    tlds = ["com", "net", "biz", "us", "info", "online", "org"]
    return tld in tlds


def valid_domain(domain):
    """Return True if domain is not blank,
    and contains a valid top level domain name."""
    # Domain cannot contain spaces, or some other special characters
    # Domain must have a valid TLD

    try:
        return valid_tld(domain.split('.')[-1])
    except IndexError:
        return False
    except ValueError:
        return False


def resolve_ip(domain_name):
    """Resolve IPV4 address from domain name"""
    #TODO remove whitespace, otherwise it won't resolve
    # Ex.: "blueequinoxconsulting.com	"
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror:
        return  # IP not resolved


def reverse_ip(ip_address):
    """Reverse the octets of an IP address"""
    return '.'.join(reversed(str(ip_address).split('.')))


def bl_lookup_by_ip(ip_address, blacklist):
    """Check ip_address against an IP blacklist.
    Query is in the form of: reversed_ip.target.blacklist.com"""
    return resolve_ip(reverse_ip(ip_address) + '.' + blacklist)


def bl_lookup_by_domain(domain, blacklist):
    """Resolve IP from domain, then check against IP blacklist"""
    return bl_lookup_by_ip(resolve_ip(domain), blacklist)


def dbl_lookup(target_domain, domain_blacklist):
    """Check target_domain against domain_blacklist.
    Query is in the form os: target_domain.domain_blacklist.com"""
    return resolve_ip(target_domain + '.' + domain_blacklist)
