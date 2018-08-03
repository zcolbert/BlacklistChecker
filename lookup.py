# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
# ===================================================================

#! python3

import ipdns
from blacklists import domain_blacklists, ip_blacklists


def get_domain():
    """Return a valid domain name from user input."""
    domain = input("Enter domain name: ")
    while not ipdns.valid_domain(domain):
        domain = input("Invalid entry. Enter domain name: ")
    return domain

def check_against_ip_blacklist(domain):
    pass

def check_against_domain_blacklist(domain):
    pass

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


if __name__ == "__main__":
    main()