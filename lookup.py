#===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
#               Domain is passed as command line argument.
#===================================================================

#! python3

import sys
import ipdns
from blacklists import domain_blacklists, ip_blacklists


def lookup(domain):

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


lookup(sys.argv[1])




