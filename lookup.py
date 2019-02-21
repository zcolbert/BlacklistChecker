#! python3
# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a single domain.
# ===================================================================

import os
import argparse
import csv
from collections import OrderedDict
from configparser import ConfigParser

from blacklist.blacklist import BlacklistType
from blacklist.blacklist import create_blacklist
from blacklist.checker import BlacklistChecker


def load_domains_from_csv(filename, domain_field, delimiter=','):
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile, delimiter=delimiter)
        return [row[domain_field] for row in reader if row[domain_field] != '']


def load_blacklists_from_csv(filename):
    blacklists = []
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile)
        for row in reader:
            zone = row['Query Zone']
            list_type = row['Query Type']
            alias = row['Alias']
            try:
                blacklists.append(create_blacklist(list_type, zone, alias))
            except ValueError:
                # Unknown blacklist type. Skip this record
                continue
    return blacklists


def create_csv_report(results, save_location):
    fieldnames = ['Domain', 'IP Address', 'Domain Status', 'IP Status']
    filename = os.path.join(save_location, 'Listed_Report.csv')

    print('Creating', filename, '... ', end='')

    with open(filename, 'w', newline='') as srcfile:
        writer = csv.DictWriter(srcfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            row = OrderedDict()
            row['Domain'] = r.domain.name

            if r.domain_is_active():
                row['IP Address'] = r.domain.ipv4_address
            else:
                row['IP Address'] = 'Offline'

            row['Domain Status'] = ', '.join([bl.alias for bl in r.domain_listings])
            row['IP Status'] = ', '.join([bl.alias for bl in r.ip_listings])
            writer.writerow(row)
    print('Done.')


def lookup(domains, checker):
    results = []
    for domain in domains:
        print('Checking', domain, '...')
        result = checker.query(domain, BlacklistType.ALL)
        results.append(result)
    return results


def get_args():
    parser = argparse.ArgumentParser(
        description='Check domain or IP against blacklists')

    parser.add_argument('-d', '--domain')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-c', '--column')
    parser.add_argument('-r', '--report')

    return parser.parse_args()


def init_domains(args, cfg):
    if args.domain:
        # lookup domain specified
        domains = [args.domain]
    elif args.filename:
        # lookup domains from file specified
        domains = load_domains_from_csv(
            args.filename, args.column)
    else:
        # load domains from default file location
        domains = load_domains_from_csv(
            cfg.get('DOMAINS', 'TestFilePath'),
            cfg.get('DOMAINS', 'Fieldname'),
            cfg.get('DOMAINS', 'Delimiter'))
    return domains


def main():

    cfg = ConfigParser()
    cfg.read('config.ini')

    args = get_args()

    domains = init_domains(args, cfg)
    blacklists = load_blacklists_from_csv(
        cfg.get('BLACKLIST', 'Blacklists'))
    checker = BlacklistChecker(blacklists)

    results = lookup(domains, checker)

    if args.report:
        save_location = args.report
    else:
        save_location = cfg.get('FILES', 'ReportSaveLocation')
    create_csv_report(results, save_location)


if __name__ == "__main__":
    main()
