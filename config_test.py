#! python3

import configparser


cfg = configparser.ConfigParser()
cfg.read("config.ini")

print(cfg.sections())
print(cfg.options(cfg.sections()[0]))
print(cfg.options(cfg.sections()[1]))

print(cfg.get("EMAIL", "SmtpServer"))