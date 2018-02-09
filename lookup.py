#!python3

import ipdns
from blacklists import domain_blacklists, ip_blacklists

ipbl = {"backscatter.spameatingmonkey.net":"Email sent to spam trap. Removed after 15 days."}


def lookup():

    domain = "blueequinoxconsulting.com"

    print("============", domain, "============\n")

    ip = ipdns.resolve_ip(domain)
    if ip is None:
        print("Unable to resolve IP")
        return 1

    for bl in ip_blacklists:
        if ipdns.bl_lookup_by_ip(ip, bl) is not None:
            print("IP is listed on:", bl)

    for dbl in domain_blacklists:
        if ipdns.dbl_lookup(domain, dbl) is not None:
            print("Domain is listed on:", dbl)

lookup()




