# =============================================================================
#   Store the domain records in a SQLite Database
# =============================================================================


import csv
import sqlite3
from configparser import ConfigParser


def export_to_csv():
    """Export the entire contents of database
    into as CSV file."""
    pass


def import_from_csv():
    """Import new records into database from CSV file.
    Contents appended into existing database."""
    pass


def create_from_csv():
    """Create database from CSV file.
    Existing database contents will be overwritten."""


def add_record():
    pass


def delete_record():
    pass


def run():
    cfg = ConfigParser()
    cfg.read("config.ini")
    domain_file = cfg.get("FILES", "DomainFile")

    # Connect to the database
    db_connection = sqlite3.connect(cfg.get("DATABASE", "DomainDB"))
    c = db_connection.cursor()  # Create a DB Cursor to perform SQL commands

    c.execute("PRAGMA foreign_keys = ON")

    c.execute('''CREATE TABLE domains(
                    DomainName TEXT PRIMARY KEY,
                    Status INTEGER,
                    Role TEXT,  
                    PrevListed INTEGER,
                    ListedOn TEXT,
                    FOREIGN KEY(ListedOn) REFERENCES blacklists(ListName))''')

    c.execute('''CREATE TABLE blacklists(
                    ListName TEXT PRIMARY KEY,
                    ListType INTEGER)''')

    c.execute('''CREATE TABLE accounts(
                    ID INTEGER,
                    Name TEXT)''')

    db_connection.commit()
    db_connection.close()

run()