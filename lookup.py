# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
# ===================================================================

#! python3

import ipdns
from blacklists import domain_blacklists, ip_blacklists


def valid_tld(tld):
    """Return True if tld is a valid top level domain"""
    tlds = ["com", "net", "biz", "us", "info", "online"]
    return tld in tlds


def valid_domain(domain):
    """Return True if domain is not blank,
    and contains a valid top level domain name."""
    try:
        return valid_tld(domain.split('.')[-1])
    except IndexError:
        return False
    except ValueError:
        return False


def get_domain():
    """Return a valid domain name from user input."""
    domain = input("Enter domain name: ")
    while not valid_domain(domain):
        domain = input("Invalid entry. Enter domain name: ")
    return domain


def lookup(domain):
    """Check domain against domain blacklists,
    and IP blacklists. Print a report of any listings."""
    times_listed = 0
    print("============", domain, "============")

    ip = ipdns.resolve_ip(domain)
    if ip is None:
        print("Unable to resolve IP")
        return 1

    for bl in ip_blacklists:
        if ipdns.bl_lookup_by_ip(ip, bl) is not None:
            print("IP is listed on:", bl)
            times_listed += 1

    for dbl in domain_blacklists:
        if ipdns.dbl_lookup(domain, dbl) is not None:
            print("Domain is listed on:", dbl)
            times_listed += 1

    if times_listed > 0:
        print("Total listings:", times_listed)
    else:
        print("No listings.")


def main():

    while True:
        lookup(get_domain())


main()




