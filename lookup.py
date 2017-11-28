#!python3

import ipdns

ipbl = {"backscatter.spameatingmonkey.net":"Email sent to spam trap. Removed after 15 days."}

ip_blacklists = ["zen.spamhaus.org",
                 "bl.spameatingmonkey.net"
                 ]

domain_blacklists = ["dbl.spamhaus.org",
                     "fresh.spameatingmonkey.net"
                     "fresh10.spameatingmonkey.net",
                     "fresh15.spameatingmonkey.net",
                     "fresh30.spameatingmonkey.net",
                     ]


def lookup():

    domain = "inspectorresources.net"

    print("============", domain, "============")

    ip = ipdns.resolve_ip(domain)
    if ip is None:
        print("Unable to resolve IP")
        return 1

    for bl in ip_blacklists:
        if ipdns.bl_lookup_by_ip(ip, bl) is not None:
            print("IP listed:", ip)

    for dbl in domain_blacklists:
        if ipdns.dbl_lookup(domain, dbl) is not None:
            print("Domain is listed on:", dbl)

lookup()




