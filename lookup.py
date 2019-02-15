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
from blacklist.blacklist import BlacklistChecker, Blacklist
from blacklist.blacklist import create_blacklist


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
    if domain.is_active():
        ip = domain.ipv4_address
    else:
        ip = "Offline"
    print('{domain} ({ip})'.format(domain=domain.name, ip=ip))
    print('{:-<48}'.format(''))

    for b in status.blacklists:
        print('{:<12} @ {:<32}'.format(
            b.query_type, b.alias
        ))
    print('\nTOTAL LISTINGS: {}'.format(len(status.blacklists)))
    print('=' * 48)
    print()


def load_blacklists_from_csv(filename):
    blacklists = []
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile)
        for row in reader:
            zone = row['Query Zone']
            list_type = row['Query Type']
            alias = row['Alias']
            blacklists.append(create_blacklist(list_type, zone, alias))
    return blacklists


def create_csv_report(results, account_name=''):
    fieldnames = ['Domain', 'IP Address', 'Domain Status', 'IP Status']
    filename = '_'.join((account_name, 'Listed_Report.csv')).strip('_')

    print('Creating', filename, '... ', end='')

    with open(filename, 'w', newline='') as srcfile:
        writer = csv.DictWriter(srcfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            row = OrderedDict()
            row['Domain'] = r.domain.name

            if r.domain.is_active():
                row['IP Address'] = r.domain.ipv4_address
            else:
                row['IP Address'] = 'Offline'

            row['Domain Status'] = ', '.join([bl.alias for bl in r.domain_listings])
            row['IP Status'] = ', '.join([bl.alias for bl in r.ip_listings])
            writer.writerow(row)
    print('Done.')


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

    results = []
    for domain in domains:
        print('Checking', domain, '...')
        results.append(lookup_domain(domain, checker))

    create_csv_report(results)


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
