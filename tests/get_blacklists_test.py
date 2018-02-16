#! python3

from ipdns import valid_domain

DBL_LIST_FILE = "../files/domain_blacklists.txt"
IP_LIST_FILE = "../files/ip_blacklists.txt"

def get_blacklists(bl_file):
    dbl_lists = []
    print("Opening", bl_file, "...")
    with open(bl_file, 'r', newline='') as file:
        for line in file:
            if valid_domain(line.strip()):
                dbl_lists.append(line)

    return dbl_lists

def test():
    print("Getting domain blacklists ...")
    dbls = get_blacklists(DBL_LIST_FILE)
    print("Found", len(dbls), "domain lists.")

    print("Getting IP blacklists ...")
    ipbls = get_blacklists(IP_LIST_FILE)
    print("Found", len(ipbls), "IP lists.")

test()
