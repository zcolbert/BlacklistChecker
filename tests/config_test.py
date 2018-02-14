#! python3

import configparser

cfg = configparser.ConfigParser()

print("Reading config file ...")
cfg.read("../config.ini")
print("Done")

print(cfg.sections())
print(cfg.get("EMAIL_OPTIONS", "SmtpServer"))
print(cfg.get("FILES", "ReportSaveLocation"))