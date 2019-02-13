#! python3
# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
# ===================================================================

import csv
import argparse
from collections import OrderedDict
from configparser import ConfigParser

from domain import Domain, DomainStatus
from blacklist.blacklist import BlacklistChecker, DomainBlacklist, IPBlacklist


def load_domains_from_csv(filename, status='', delimiter=',', domain_field='Domain'):
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile, delimiter=delimiter)
        if status != '':
            return [Domain(row[domain_field]) for row in reader if row['Status' == status]]
        else:
            return [Domain(row[domain_field]) for row in reader if row[domain_field] != '']


def print_blacklist_report(status):
    print('=' * 48)
    domain = status.domain
    print('{domain} ({ip})'.format(
        domain=domain.name, ip=domain.ipv4_address))
    print('{:-<48}'.format(''))
    for b in status.blacklists:
        print('{:<12} @ {:<32}'.format(
            b.query_type, b.alias
        ))
    print('\nTOTAL LISTINGS: {}'.format(len(status.blacklists)))
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


def lookup_domain(domain, checker):
    if domain.is_active():
        return checker.query(domain)
    else:
        return DomainStatus(domain, status='Offline')


def lookup_domains():

    cfg = ConfigParser()
    cfg.read('config.ini')

    blacklists = load_blacklists_from_csv(cfg.get('BLACKLIST', 'Blacklists'))
    checker = BlacklistChecker(blacklists)
    domains = load_domains_from_csv('C:/Users/Zachary/Desktop/servers.csv', delimiter=',')

    for domain in domains:
        result = lookup_domain(domain, checker)
        print_blacklist_report(result)

    #create_csv_report(checker.get_listed_domains())


def get_args():

    parser = argparse.ArgumentParser(description='Check domain or IP against blacklists')

    parser.add_argument('domain')
    parser.add_argument('-i', '--ip-address', action='store_true', default=False, dest='lookup_ip')
    parser.add_argument('-d', '--domain-name', action='store_true', default=False, dest='lookup_domain')
    # -f --file

    args = parser.parse_args()

    domain = args.domain
    if args.lookup_ip:
        print('Looking up IP')
    elif args.lookup_domain:
        print('Looking up domain')
    else:
        print('Looking up all')




if __name__ == "__main__":
    lookup_domains()
