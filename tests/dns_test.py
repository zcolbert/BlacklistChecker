#! python3

from main import retrieve_blacklists
import ipdns

def test():
    ipbls = retrieve_blacklists("../files/ip_blacklists.txt")
    dbls = retrieve_blacklists("../files/domain_blacklists.txt")

    print("IP Blacklists:", len(ipbls))
    print(ipbls, '\n')
    print("Domain Blacklists:", len(dbls))
    print(dbls, '\n')

    for bl in ipbls:
        if not ipdns.valid_domain(bl):
            print("Invalid:", bl)

    for dbl in dbls:
        if not ipdns.valid_domain(dbl):
            print("Invalid:", dbl)

test()