#! python3

import csv
import ipdns
from blacklists import bls, dbls
from domains import domains
import datetime

REPORT_FILE = "blacklist_report_%s.csv" % datetime.date.today().strftime("%m-%d-%Y")

bl = "zen.spamhaus.org"
dbl = "dbl.spamhaus.org"

def main():

    with open(REPORT_FILE, 'w', newline="") as report:
        writer = csv.writer(report, dialect='excel')
        writer.writerow(["Domain Name", "IP Address", "Listed On", "List Type"])

        for domain in domains:

            print("Checking", domain, "...")
            ip = ipdns.resolve_ip(domain)
            ip_status = ipdns.bl_lookup_by_ip(ip, bl)
            dns_status = ipdns.dbl_lookup(domain, dbl)

            if not ip_status == None:
                print(domain, " - IP is listed", ip)
                writer.writerow([domain, ip, bl, "IP Address"])

            if not dns_status == None:
                print(domain, "is listed on", dbl)
                writer.writerow([domain, ip, dbl, "Domain"])


main()