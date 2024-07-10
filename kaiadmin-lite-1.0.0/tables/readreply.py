import imaplib
import email
import csv
from datetime import datetime
from dateutil import parser as date_parser
import re

imap_server = "imap.gmail.com"
imap_port = 993

# Your Gmail credentials
username = "galianoanthony581@gmail.com"
password = "itgu frua gmix mapn"

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)

try:
    # Login to your account
    mail.login(username, password)
    mail.select("inbox")
    status, response = mail.search(None, 'ALL')
    email_ids = response[0].split()
    # sort the emails in reverse order to get the latest email first
    latest_emails = email_ids[::-1][:25]
    # Prepare CSV file to store emails
    csv_filename = "email_details.csv"
    mailerdaemon_csv_filename = "mailerdaemon.csv"

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file, \
         open(mailerdaemon_csv_filename, 'w', newline='', encoding='utf-8') as mailerdaemon_csv_file:

        csv_writer = csv.writer(csv_file, delimiter='^')  # Specify delimiter as ^
        csv_writer.writerow(['Date', 'Sender', 'Subject'])

        mailerdaemon_csv_writer = csv.writer(mailerdaemon_csv_file, delimiter='^')
        mailerdaemon_csv_writer.writerow(['Date', 'Sender', 'Subject'])

        # Function to format date
        def format_date(date_str):
            dt = date_parser.parse(date_str)
            formatted_date = dt.strftime("%a, %d %b %Y %H:%M:%S")
            return formatted_date

        # Function to extract email address from 'From' header
        def extract_email_from_header(header):
            match = email.utils.parseaddr(header)[1]
            return match

        # Function to extract email address from email body
        def extract_email_from_body(body):
            pattern = r'[\w\.-]+@[\w\.-]+'
            match = re.search(pattern, body)
            if match:
                return match.group(0)
            else:
                return ""

        # Fetch each email and extract required fields
        for email_id in latest_emails:
            status, data = mail.fetch(email_id, "(RFC822)")
            if status == 'OK':
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract necessary fields
                date = format_date(msg['Date']) if msg['Date'] else ""
                sender = extract_email_from_header(msg['From']) if msg['From'] else ""
                subject = msg['Subject'] if msg['Subject'] else ""
                body = ""

                # Extract body content
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                        break

                # Check if the email is from mailer daemon
                if sender.strip().lower() == 'mailer-daemon@googlemail.com':
                    email_from_body = extract_email_from_body(body)
                    mailerdaemon_csv_writer.writerow([date, email_from_body, subject])
                else:
                    csv_writer.writerow([date, sender, subject])
            else:
                print(f"Failed to fetch email with ID: {email_id}")

    print(f"Email details (date, sender, subject) of last 25 emails saved to {csv_filename}")
    print(f"Mailer daemon emails saved to {mailerdaemon_csv_filename}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Logout from the mailbox
    mail.logout()
