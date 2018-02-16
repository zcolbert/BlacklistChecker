#! python3

import os
import csv
import datetime
import ipdns
from domains import DomainRecord, ListedDomain
from mailer import SSLMailer, MessageTemplate
from configparser import ConfigParser


CONFIG_FILE = "config.ini"
MSG_TEMPLATE = "files/email_template.txt"
DOMAIN_FILE = "C:\\Users\\Zachary\\Documents\\IBW\\Accounts\\domains.csv"
REPORT_FILE = "blacklist_report_%s.csv" % datetime.date.today().strftime("%m-%d-%Y")


def load_domain_list():
    """Load the list of active customer domains
    into an array of DomainRecord objects."""
    domains = []
    with open(DOMAIN_FILE, 'r') as file:
        reader = csv.DictReader(file, dialect='excel')

        for row in reader:
            if row["Domain"] != "" and row["Status"] == "Active":
                temp_row = DomainRecord()
                temp_row.name = row["Domain"]
                temp_row.role = row["Role"]
                temp_row.master = row["Master"]
                temp_row.account = row["IBW Account Name"]
                temp_row.acct_id = row["IBW Account ID"]

                domains.append(temp_row)

    return domains


def get_blacklists(bl_file):
    """Return array of blacklist domains read from bl_file."""
    dbl_lists = []
    with open(bl_file, 'r') as file:
        for line in file:
            if ipdns.valid_domain(line.strip()):
                dbl_lists.append(line.strip())

    return dbl_lists


def lookup_domains(domain_list):
    """Check each domain against the IP Blacklists and Domain Blacklists.
    The IP lookup will return a result if the IP or Domain is listed.
    Otherwise, the lookup will return None"""
    cfg = ConfigParser()
    cfg.read(CONFIG_FILE)

    ip_blacklists = get_blacklists(cfg.get("BLACKLIST", "IP_Lists"))
    domain_blacklists = get_blacklists(cfg.get("BLACKLIST", "DBL_Lists"))

    listed_domains = []
    inactive_domains = []

    for domain in domain_list:
        print("Checking", domain.name, "...")
        ip = ipdns.resolve_ip(domain.name)

        if ip is None:
            inactive_domains.append(domain.name)
            continue  # skip this domain

        # Check against IP blacklists
        for bl in ip_blacklists:
            ip_status = ipdns.bl_lookup_by_ip(ip, bl)
            if ip_status is not None:  # IP is listed
                temp_domain = ListedDomain(domain, ip, bl, "IP Address")
                listed_domains.append(temp_domain)

        # Check against Domain blacklists
        for dbl in domain_blacklists:
            dns_status = ipdns.dbl_lookup(domain.name, dbl)
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


def generate_report(listed_domains):
    """Create a CSV report containing
    information about each listed domain"""
    cfg = ConfigParser()
    cfg.read(CONFIG_FILE)

    filename = "blacklist_report_%s.csv" % datetime.date.today().strftime("%m-%d-%Y")
    report_file = os.path.join(cfg.get("FILES", "ReportSaveLocation"), filename)

    with open(report_file, 'w', newline="") as report:
        writer = csv.writer(report, dialect='excel')
        writer.writerow(["Account", "ID", "Domain Name", "IP Address",
                         "Listed On", "List Type", "Previously Blacklisted"])

        for domain in listed_domains:
            writer.writerow([domain.account,
                             domain.acct_id,
                             domain.name,
                             domain.ip_address,
                             domain.list_name,
                             domain.list_type,
                             domain.prev_listed])


def generate_email_template(listed_domains, template_file):
    """Generate a file to be used as the email body.
    File contains information about each listed
    domain in an HTML Table format."""
    with open(template_file, 'w') as msg_file:
        msg = MessageTemplate(msg_file)
        msg.generate_template_header()
        # Write the rows for each listed domain
        for domain in listed_domains:
            fields = [domain.acct_id,
                      domain.name,
                      domain.ip_address,
                      domain.list_name,
                      domain.list_type]

            msg.write_table_row(fields)

        msg.generate_template_footer()


def send_report_email(recipient, message_template):
    """Send the report email to the recipient"""
    cfg = ConfigParser()
    cfg.read(CONFIG_FILE)

    print("Sending report email ...")
    try:
        mailer = SSLMailer(cfg.get("EMAIL_OPTIONS", "SmtpServer"),
                           cfg.get("EMAIL_OPTIONS", "SSLPort"),
                           cfg.get("EMAIL_OPTIONS", "UserName"),
                           cfg.get("EMAIL_OPTIONS", "SmtpPasswd"),
                           message_template)
        mailer.send(recipient)
        print("Email sent successfully")
    except:
        print("Sending failed")
        with open("email_error.txt", 'a') as logfile:
            logfile.write("%s\t%s\t\n"
                          % ("Sending failed",
                             datetime.date.today().strftime("%m-%d-%Y")))


def main():
    domains = load_domain_list()
    # Check each of the domains against the BL and DBL
    listed_domains = lookup_domains(domains)  # Contains ListedDomain objects
    generate_report(listed_domains)
    generate_email_template(listed_domains, MSG_TEMPLATE)
    #send_report_email("support@myzensend.com", MSG_TEMPLATE)


if __name__ == "__main__":
    main()
