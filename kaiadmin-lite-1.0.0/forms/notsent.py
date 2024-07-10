import imaplib
import email
import csv
from email.header import decode_header

# IMAP settings
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Gmail credentials (enable Less Secure Apps in Google Account settings)
username = "galianoanthony581@gmail.com"
password = "itgu frua gmix mapn"  # Your Gmail password

# Connect to Gmail's IMAP server
mail = imaplib.IMAP4_SSL(smtp_server)
mail.login(username, password)
mail.select("inbox")  # Select the inbox folder

# Search for emails from mailer-daemon@googlemail.com
status, data = mail.search(None, '(FROM "mailer-daemon@googlemail.com")')

if status == "OK":
    email_ids = data[0].split()
    for email_id in email_ids:
        # Fetch the email
        status, data = mail.fetch(email_id, "(RFC822)")
        if status == "OK":
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract email content
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if "plain" in content_type:
                        body = part.get_payload(decode=True).decode()
                        # Extract email address from the body
                        if "non è stato recapitato perché" in body:
                            start_index = body.find("perché") + len("perché")
                            end_index = body.find("risulta inesistente.")
                            if start_index != -1 and end_index != -1:
                                email_address = body[start_index:end_index].strip()
                                
                                # Search for the email in the CSV file and update
                                with open('lodgings - Copia.csv', newline='', mode='r') as file:
                                    reader = csv.reader(file)
                                    rows = list(reader)
                                    for row in rows:
                                        if row[0] == email_address:
                                            # Update the CSV with "not sent column" = "1"
                                            row.append("1")  # Assuming the last column is "not sent column"
                                            break
                                
                                # Rewrite the CSV file with updated information
                                with open('lodgings - Copia.csv', 'w', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerows(rows)
                                    print(f"Updated CSV for email: {email_address}")

# Close the connection
mail.logout()
