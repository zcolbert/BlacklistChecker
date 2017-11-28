#===================================================================================================
#   Module name:    mailer.py
#   Author:         Zachary Colbert zcolbert1993@gmail.com
#   Date:           11-26-2017
#   Purpose:        Generate email message templates, and send a message
#                   via SSL based email server.
#===================================================================================================

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SSLMailer:
    """Send a message via SSL based email server"""
    def __init__(self, server, port, username, password, message_template):
        self.message_template = message_template
        self.server = smtplib.SMTP_SSL(server, port)
        self.server.login(username, password)
        self.msg = MIMEMultipart()
        self.initialize_message_header()
        self.read_template()

    def initialize_message_header(self):
        today = datetime.date.today().strftime("%m-%d-%Y")
        self.msg["Subject"] = "Blacklist Report " + today
        self.msg["From"] = "support@myzensend.com"
        self.msg.preamble = "Blacklist Report " + today

    def read_template(self):
        """Create the message body from the supplied template file"""
        with open(self.message_template) as template:
            html_content = template.read()
        self.msg.attach(MIMEText(html_content, "html"))

    def send(self, recipient):
        self.msg["To"] = recipient
        text = self.msg.as_string()
        self.server.sendmail(self.msg["From"], self.msg["To"], text)


class MessageTemplate:
    """Write an HTML email message template to the file_stream"""
    def __init__(self, file_stream):
        self.file_stream = file_stream

    def write_html_header(self):
        """Write the opening boilerplate tags for an HTML document"""
        self.file_stream.write("<!DOCTYPE html>\n\n")
        self.file_stream.write("<html>\n")
        self.file_stream.write("\t<head></head>\n")
        self.file_stream.write("\t<body>\n")

    def write_html_footer(self):
        """Write the closing boilerplate tags for an HTML document"""
        self.file_stream.write("\t</body>\n")
        self.file_stream.write("</html>\n")

    def write_table_header(self):
        """Write the opening tags for an HTML table"""
        self.file_stream.write("\t\t<table border=\"1\" width=\"100%\" cellpadding=\"2\" cellspacing=\"2\">\n")
        self.file_stream.write("\t\t\t<tbody>\n")
        # Write the contents of the header row
        self.file_stream.write("\t\t\t\t<tr>\n")
        self.file_stream.write("\t\t\t\t\t<td>Domain Name</td>\n")
        self.file_stream.write("\t\t\t\t\t<td>IP Address</td>\n")
        self.file_stream.write("\t\t\t\t\t<td>Listed On</td>\n")
        self.file_stream.write("\t\t\t\t\t<td>List Type</td>\n")
        self.file_stream.write("\t\t\t\t</tr>\n")

    def write_table_row(self, c1, c2, c3, c4):
        """Write a table row (with 4 columns)"""
        self.file_stream.write("\t\t\t\t<tr>\n")
        self.file_stream.write("\t\t\t\t\t<td>" + c1 + "</td>\n")
        self.file_stream.write("\t\t\t\t\t<td>" + c2 + "</td>\n")
        self.file_stream.write("\t\t\t\t\t<td>" + c3 + "</td>\n")
        self.file_stream.write("\t\t\t\t\t<td>" + c4 + "</td>\n")
        self.file_stream.write("\t\t\t\t</tr>\n")

    def write_table_footer(self):
        """Write the closing tags for an HTML table"""
        self.file_stream.write("\t\t\t</tbody>\n")
        self.file_stream.write("\t\t</table>\n")

    def generate_template_header(self):
        """Generate the template file's opening tags"""
        self.write_html_header()
        self.write_table_header()

    def generate_template_footer(self):
        """Generate the template file's closing tags and datestamp"""
        dt = datetime.datetime.today().strftime("%m-%d-%y @ %I:%M %p")
        self.write_table_footer()
        self.file_stream.write("\t\t<br><p>Report generated: " + dt + "</p>\n")
        self.write_html_footer()


def test():
    test_mailer = SSLMailer("shinari.websitewelcome.com", 465,
                            "support@myzensend.com", "Paso93447",
                            "files/email_template.txt")
    print(test_mailer.msg)
    test_mailer.send("zac@inboxwired.com")
