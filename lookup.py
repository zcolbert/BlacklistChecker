#! python3
# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a set of domains.
# ===================================================================

import os
import argparse
import csv

from typing import List, Sequence

import dnstools
from collections import OrderedDict
from configparser import ConfigParser

from blacklist.blacklist import Blacklist
from blacklist.blacklist import create_blacklist
from blacklist.checker import BlacklistChecker, DomainStatus


def load_hostnames_from_csv(filename: str, host_field: str, delimiter: str = ',') -> List[str]:
    with open(filename, 'r') as srcfile:
        reader = csv.DictReader(srcfile, delimiter=delimiter)
        return [row[host_field] for row in reader if row[host_field] != '']


def load_blacklists_from_csv(filename: str) -> List[Blacklist]:
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


def create_csv_report(results: Sequence[DomainStatus], save_location: str):
    fieldnames = ['Domain', 'IP Address', 'Domain Status', 'IP Status']
    filename = os.path.join(save_location, 'Listed_Report.csv')

    print('Creating', filename, '... ', end='')

    with open(filename, 'w', newline='') as srcfile:
        writer = csv.DictWriter(srcfile, fieldnames=fieldnames)
        writer.writeheader()

        for r in results:
            row = OrderedDict()
            row['Domain'] = r.domain.hostname

            if dnstools.host_is_active(r.domain.hostname):
                row['IP Address'] = r.domain.ipv4_address
            else:
                row['IP Address'] = 'Offline'

            row['Domain Status'] = ', '.join([bl.alias for bl in r.domain_listings])
            row['IP Status'] = ', '.join([bl.alias for bl in r.ip_listings])
            writer.writerow(row)
    print('Done.')


def get_args():
    parser = argparse.ArgumentParser(
        description='Check domain or IP against blacklists')

    parser.add_argument('-d', '--domain')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-c', '--column')
    parser.add_argument('-r', '--report')
    parser.add_argument('-p', '--print', action='store_true', default=False)

    return parser.parse_args()


def init_domains(args, cfg: ConfigParser) -> List[str]:
    if args.domain:
        # lookup a single specified domain
        domains = [args.domain]
    elif args.filename:
        # lookup domains from indicated file
        domains = load_hostnames_from_csv(
            args.filename, args.column)
    else:
        # load domains from default file location
        domains = load_hostnames_from_csv(
            cfg.get('DOMAINS', 'FilePath'),
            cfg.get('DOMAINS', 'Fieldname'),
            cfg.get('DOMAINS', 'Delimiter'))
    return domains


def lookup_hostnames(checker: BlacklistChecker, hostnames: Sequence[str], verbose=False) -> List[DomainStatus]:
    results = []
    for host in hostnames:
        if verbose:
            print(f'Looking up {host} ... ', end='')
        result = checker.query(host)
        if verbose:
            print(result.status)
        results.append(result)
    return results


def main():

    cfg = ConfigParser()
    cfg.read('config.ini')

    args = get_args()

    domains = init_domains(args, cfg)

    blacklists = load_blacklists_from_csv(
        cfg.get('BLACKLIST', 'Blacklists'))

    checker = BlacklistChecker(blacklists)
    results = lookup_hostnames(checker, domains, verbose=args.print)

    if args.report:
        save_location = args.report
    else:
        save_location = cfg.get('FILES', 'ReportSaveLocation')
    create_csv_report(results, save_location)


if __name__ == "__main__":
    main()
