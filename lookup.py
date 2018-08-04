#! python3
# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
# ===================================================================

import csv
import ipdns
from blacklist import IPBlacklist, DomainBlacklist, ListedDomain, BlacklistChecker
from socket import gaierror

DOMAIN_FILE = 'C:/Users/Zachary/Documents/IBW/Accounts/domains_csv.csv'


def get_active_domains():
    with open(DOMAIN_FILE, 'r') as domain_file:
        reader = csv.DictReader(domain_file)
        for row in reader:
            return [row['Domain'] for row in reader if row['Status'] == 'Active']


def lookup_domains_by_ip(domains):
    with open(DOMAIN_FILE, 'r') as domain_file:
        reader = csv.DictReader(domain_file)
        for row in reader:
            if row['Status'] == 'Active':
                print('Account is active:', row['IBW Account Name'])


def init_blacklists(bl_file):
    pass


def main():
    blacklists = init_blacklists('')
    checker = BlacklistChecker(blacklists)

    active = get_active_domains()
    active_domains = [ipdns.Domain(a) for a in active]

    blacklist = DomainBlacklist('dbl.spamhaus.org')
    for domain in active_domains:
        try:
            checker.check_against_blacklist(domain, blacklist)
        except gaierror:
            print('Domain is inactive:', domain.name)

    print('Total listed domains:', len(checker.listed_domains))

    listed = checker.get_listed_domains()
    for d in listed:
        print(d)

if __name__ == "__main__":
    main()