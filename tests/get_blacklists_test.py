#! python3

from main import get_blacklists
from ipdns import valid_domain

DBL_LIST_FILE = "../files/domain_blacklists.txt"
IP_LIST_FILE = "../files/ip_blacklists.txt"


def test():
    print("Getting domain blacklists ...")
    dbls = get_blacklists(DBL_LIST_FILE)
    print("Found", len(dbls), "domain lists.")
    print(dbls)

    print("Getting IP blacklists ...")
    ipbls = get_blacklists(IP_LIST_FILE)
    print("Found", len(ipbls), "IP lists.")
    print(ipbls)

test()
