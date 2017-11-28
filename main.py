#!python3

import csv
import datetime
import ipdns
from domains import domains, ListedDomain
from mailer import SSLMailer, MessageTemplate

MSG_TEMPLATE = "files/email_template.txt"
REPORT_FILE = "blacklist_report_%s.csv" % datetime.date.today().strftime("%m-%d-%Y")


def lookup_domains():
    """Check each domain against the IP blacklist, and Domain Blacklist.
    The IP lookup will return a result if the IP or Domain is listed."""

    #bl = "zen.spamhaus.org"     # IP Blacklist
    #dbl = "dbl.spamhaus.org"    # Domain Blacklist

    ip_blacklists = ["zen.spamhaus.org",
                     "bl.spameatingmonkey.net"
                     ]

    domain_blacklists = ["dbl.spamhaus.org",
                         "fresh.spameatingmonkey.net"
                         "fresh10.spameatingmonkey.net",
                         "fresh15.spameatingmonkey.net",
                         "fresh30.spameatingmonkey.net",
                         ]

    listed_domains = []
    inactive_domains = []

    for domain in domains:
        print("Checking", domain, "...")
        ip = ipdns.resolve_ip(domain)
        if ip is None:
            inactive_domains.append(domain)
            continue  # skip this domain

        # Check against IP blacklists
        for bl in ip_blacklists:
            ip_status = ipdns.bl_lookup_by_ip(ip, bl)
            if ip_status is not None:  # IP is listed
                temp_domain = ListedDomain(domain, ip, bl, "IP Address")
                listed_domains.append(temp_domain)

        # Check against Domain blacklist
        for dbl in domain_blacklists:
            dns_status = ipdns.dbl_lookup(domain, dbl)
            if dns_status is not None:  # Domain is listed
                temp_domain = ListedDomain(domain, ip, dbl, "Domain")
                listed_domains.append(temp_domain)

    # Create a log file of potentially inactive domains
    log_inactive_domains(inactive_domains)

    return listed_domains


def log_inactive_domains(inactive_domains):
    domain_file = "files/inactive_domains.txt"
    with open(domain_file, 'w') as file:
        for domain in inactive_domains:
            file.write(domain + "\n")


def generate_report(listed_domains, report_file):
    """Create a CSV report containing
    information about each listed domain"""
    with open(report_file, 'w', newline="") as report:
        writer = csv.writer(report, dialect='excel')
        writer.writerow(["Domain Name", "IP Address", "Listed On", "List Type"])

        for domain in listed_domains:
            writer.writerow([domain.domain_name,
                             domain.ip_address,
                             domain.list_name,
                             domain.list_type])


def generate_email_template(listed_domains, template_file):
    """Generate a file to be used as the email body.
    File contains information about each listed
    domain in an HTML Table format."""
    with open(template_file, 'w') as msg_file:
        msg = MessageTemplate(msg_file)
        msg.generate_template_header()
        # Write the rows for each listed domain
        for domain in listed_domains:
            msg.write_table_row(domain.domain_name,
                                domain.ip_address,
                                domain.list_name,
                                domain.list_type)
        msg.generate_template_footer()


def send_report_email(recipient, message_template):
    """Send the report email to the recipient"""
    mailer = SSLMailer("shinari.websitewelcome.com", 465,
                       "support@myzensend.com", "Paso93447",
                        message_template)
    mailer.send(recipient)


def main():

    # Check each of the domains against the BL and DBL
    listed_domains = lookup_domains()  # Contains ListedDomain objects
    generate_email_template(listed_domains, MSG_TEMPLATE)
    send_report_email("support@myzensend.com", MSG_TEMPLATE)


main()
