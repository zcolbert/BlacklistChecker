#! python3
# ===================================================================
# Module Name:  lookup.py
# Purpose:      Lookup blacklist status of a set of domains.
# ===================================================================

import argparse
import csv
import datetime
import logging
import os

from typing import List, Dict, Sequence
from configparser import ConfigParser

import dnstools
from blacklist.blacklist import Blacklist
from blacklist.blacklist import create_blacklist
from blacklist.checker import BlacklistChecker, DomainStatus


def load_hostnames_from_csv(filename: str, host_field: str, delimiter: str = ',') -> List[str]:
    """Load a list of hostnames from a csv file."""
    logging.info(f'Loading hostnames from {filename} ...')
    try:
        with open(filename, 'r') as srcfile:
            reader = csv.DictReader(srcfile, delimiter=delimiter)
            return [row[host_field] for row in reader if row[host_field] != '']
    except FileNotFoundError:
        logging.critical(f"Failed to load hostnames from '{filename}': File not found")
        raise


def load_blacklists_from_csv(filename: str, fieldnames: Dict[str, str]) -> List[Blacklist]:
    """Initialize a list of Domain and IP blacklists from a csv file."""
    blacklists = []
    try:
        with open(filename, 'r') as srcfile:
            reader = csv.DictReader(srcfile)
            for row in reader:
                zone = row[fieldnames['zone']]
                list_type = row[fieldnames['type']]
                alias = row[fieldnames['alias']]
                try:
                    blacklists.append(create_blacklist(list_type, zone, alias))
                except ValueError:
                    # Unknown blacklist type. Skip this record
                    continue
        return blacklists
    except FileNotFoundError:
        logging.critical(f"Failed to load blacklists from '{filename}': File not found")
        raise


def create_csv_report(results: Sequence[DomainStatus], save_location: str):
    """Write domain and IP blacklist status to the specified CSV file."""
    fieldnames = ['Domain', 'IP Address', 'Domain Status', 'IP Status']
    filename = os.path.join(save_location, 'Listed_Report.csv')

    logging.info(f'Creating {filename} ...')

    try:
        with open(filename, 'w', newline='') as srcfile:
            writer = csv.DictWriter(srcfile, fieldnames=fieldnames)
            writer.writeheader()

            for r in results:
                row = dict()
                row['Domain'] = r.domain.hostname

                # Record IP address, or 'Offline' if the domain is not in use
                if dnstools.host_is_active(r.domain.hostname):
                    row['IP Address'] = r.domain.ipv4_address
                else:
                    row['IP Address'] = 'Offline'

                row['Domain Status'] = ', '.join([bl.alias for bl in r.domain_listings])
                row['IP Status'] = ', '.join([bl.alias for bl in r.ip_listings])
                writer.writerow(row)
        logging.info('File created successfully')
    except PermissionError:
        # File IO Error (file is likely open already)
        logging.error('Failed to create report file: Permission denied')


def get_args():
    """Retrieve and parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Check domain or IP against blacklists')

    parser.add_argument('-d', '--domain')
    parser.add_argument('-f', '--filename')
    parser.add_argument('-c', '--column')
    parser.add_argument('-r', '--report')
    parser.add_argument('-v', '--verbose', action='store_true')

    return parser.parse_args()


def init_domains(args, cfg: ConfigParser) -> List[str]:
    if args.domain:
        # lookup a single specified domain
        logging.info(f'Hostname {args.domain} supplied from command line')
        domains = [args.domain]
    elif args.filename:
        # lookup domains from indicated file
        domains = load_hostnames_from_csv(
            args.filename, args.column)
        logging.info(f'Loaded {len(domains)} successfully')
    else:
        # load domains from default file location
        domains = load_hostnames_from_csv(
            cfg.get('DOMAINS', 'FilePath'),
            cfg.get('DOMAINS', 'FieldName'),
            cfg.get('DOMAINS', 'Delimiter'))

    logging.info(f'Loaded {len(domains)} hostnames successfully')
    return domains


def lookup_hostnames(checker: BlacklistChecker, hostnames: Sequence[str]) -> List[DomainStatus]:
    """Look up blacklist status of each hostname
    and return a list of DomainStatus results."""
    logging.info(f'Checking {len(hostnames)} domains ...')
    results = []
    for host in hostnames:
        result = checker.query(host)
        log_domain_status(result)
        results.append(result)
    logging.info('Lookup completed')
    return results


def log_domain_status(status: DomainStatus):
    """Write the listing status of a domain to the log."""
    domain = status.domain
    if status.domain_is_listed():
        logging.info(f'\t{domain.hostname} listed ({len(status.domain_listings)})')
    if status.ip_is_listed():
        logging.info(f'\t{domain.ipv4_address} listed ({len(status.ip_listings)})')


def init_logger(args, config):
    """Initialize the logger configuration."""
    # set log file path string
    today = datetime.datetime.today().strftime('%m-%d-%y')
    log_path = os.path.join('logs', f'{today}.log')

    # set log level threshold
    log_level = logging.WARNING
    if args.verbose:
        log_level = logging.INFO
    if config.get('SYSTEM', 'TestMode') == True:
        log_level = logging.DEBUG

    # apply settings to default logger
    logging.basicConfig(
        format='%(asctime)s %(message)s',   # prefix each log entry with timestamp
        filename=log_path,                  # set log output path
        level=log_level)                    # set log level threshold


def main():

    cfg = ConfigParser()
    cfg.read('config.ini')

    args = get_args()
    init_logger(args, cfg)

    domains = init_domains(args, cfg)
    blacklists = load_blacklists_from_csv(
        cfg.get('BLACKLIST', 'FilePath'),
        fieldnames={
            'zone': cfg.get('BLACKLIST', 'QueryZoneFieldName'),
            'type': cfg.get('BLACKLIST', 'QueryTypeFieldName'),
            'alias': cfg.get('BLACKLIST', 'AliasFieldName')
        }
    )
    checker = BlacklistChecker(blacklists)
    results = lookup_hostnames(checker, domains)

    # determine report save location
    if args.report:
        save_location = args.report
    else:
        save_location = cfg.get('REPORT', 'SaveLocation')

    create_csv_report(results, save_location)


if __name__ == "__main__":
    main()
