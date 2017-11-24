import socket


def resolve_ip(domain_name):
    """Resolve IPV4 address from domain name"""
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror:
        return  # IP not resolved


def reverse_ip(ip_address):
    """Reverse the octets of an IP address"""
    return '.'.join(reversed(str(ip_address).split('.')))


def bl_lookup_by_ip(ip_address, blacklist):
    """Check ip_address against an IP blacklist"""
    return resolve_ip(reverse_ip(ip_address) + '.' + blacklist)


def bl_lookup_by_domain(domain, blacklist):
    """Resolve IP from domain, then check against IP blacklist"""
    return bl_lookup_by_ip(resolve_ip(domain), blacklist)


def dbl_lookup(target_domain, domain_blacklist):
    """Check target_domain against domain_blacklist"""
    return resolve_ip(target_domain + '.' + domain_blacklist)
