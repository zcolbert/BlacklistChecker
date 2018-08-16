#! python3
# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
# ===================================================================

import csv
from collections import OrderedDict
from configparser import ConfigParser
from domain import Domain
from blacklist import IPBlacklist, DomainBlacklist, ListedDomain, BlacklistChecker


def load_domains_from_csv(filename, status='', key='Domain'):
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile)
        if status != '':
            return [Domain(row[key]) for row in reader if row['Status' == status]]
        else:
            return [Domain(row[key]) for row in reader]


def load_domains_from_excel(filename, status='', key='Domain'):
    pass


def lookup_domain(domain, checker):
    print('=' * 48)
    print('{} ({})'.format(
        domain.name, domain.get_ipv4()))
    print('{:-<48}'.format(''))
    if domain.is_active():
        checker.check_against_all_blacklists(domain)

        if checker.domain_is_listed(domain):
            results = checker.get_listing_info(domain)
            for r in results:
                print('{:<12} @ {:<32}'.format(
                    r.query_type, r.alias
                ))
            print()
            print('TOTAL LISTINGS:', len(results))
    else:
        print('Domain is inactive.')
    print('=' * 48)
    print()


def load_blacklists_from_csv(filename):
    lists = []
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile)
        for row in reader:
            zone = row['Query Zone']
            list_type = row['Query Type']
            if list_type == 'Domain':
                lists.append(DomainBlacklist(zone, alias=row['Alias']))
            elif list_type == 'IP Address':
                lists.append(IPBlacklist(zone, alias=row['Alias']))
            else:
                continue
    return lists


def create_csv_report(listed_domains, account_name=''):
    fieldnames = ['Domain', 'IP', 'Domain Listed', 'IP Listed']
    filename = '_'.join((account_name, 'Listed_Report.csv')).strip('_')
    with open(filename, 'w', newline='') as srcfile:
        writer = csv.DictWriter(srcfile, fieldnames=fieldnames)
        writer.writeheader()

        for domain in listed_domains:
            row = OrderedDict()
            row['Domain'] = domain.name
            row['IP'] = domain.get_ipv4()
            row['Domain Listed'] = domain.domain_is_listed()
            row['IP Listed'] = domain.ip_is_listed()
            writer.writerow(row)


def lookup_domains():

    cfg = ConfigParser()
    cfg.read('config.ini')

    #domain_file = 'C:/Users/Zachary/Documents/IBW/Accounts/BIDX/domains.csv'
    #domains = load_domains_from_csv(domain_file)

    blacklists = load_blacklists_from_csv(cfg.get('BLACKLIST', 'Blacklists'))

    checker = BlacklistChecker(blacklists)

    domain = Domain('savemydentalpractice.com')
    lookup_domain(domain, checker)

    #for d in domains:
    #    lookup_domain(d, checker)

    #create_csv_report(checker.get_listed_domains(), account_name='BIDX')

if __name__ == "__main__":
    lookup_domains()
