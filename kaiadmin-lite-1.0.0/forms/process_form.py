import cgi
import csv
import smtplib
import time
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import os
import sys

# Sender details
sender_email = "galianoanthony581@gmail.com"
subject_template = "%NOMEHOTEL% Proposta di Efficientamento Energetico"

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Gmail SMTP port

# Your Gmail credentials
username = "galianoanthony581@gmail.com"
password = "itgu frua gmix mapn"

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

# Function to read HTML email body from file
def read_email_body(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        return file.read()

# Function to read recipient emails from the CSV file
def read_recipient_emails(csv_file):
    recipient_emails = []
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for row in csvreader:
            if len(row) >= 2:  # Ensure at least 2 columns are present
                hotel_name = row[0].strip()
                email = row[1].strip()  # Second column for email
                sent_status = row[3].strip() if len(row) >= 4 else ''  # Fourth column for sent status if present
                if email and is_valid_email(email):
                    recipient_emails.append((email, hotel_name, sent_status))
                else:
                    print(f"Skipping invalid email: {email}")
            else:
                print(f"Skipping invalid row: {row}")
    return recipient_emails

# Main function to send emails
def send_emails(recipient_csv, email_html, num_emails_to_send):
    email_body_template = read_email_body(email_html)
    recipient_emails = read_recipient_emails(recipient_csv)

    if not recipient_emails:
        print("No valid recipient emails found. Exiting.")
        return

    # Create SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption
    server.login(username, password)

    emails_sent = 0
    start_time = time.time()

    # Check if campaigns.csv exists, create if not
    if not os.path.exists("campaigns.csv"):
        with open("campaigns.csv", mode='w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';')
            csvwriter.writerow(['Hotel Name', 'Email', 'Status'])
    
    # Open CSV file in append mode to update sent status
    with open("campaigns.csv", mode='a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        
        for recipient_email, hotel_name, sent_status in recipient_emails:
            if sent_status == '1':
                print(f"Email to {recipient_email} already sent.")
                csvwriter.writerow([hotel_name, recipient_email, 'Already Sent'])  # Keep the sent status as 1
                continue

            if emails_sent >= num_emails_to_send:
                elapsed_time = time.time() - start_time
                if elapsed_time < 3600:  # If less than an hour has passed
                    sleep_time = 3600 - elapsed_time
                    print(f"Hourly limit reached. Sleeping for {sleep_time} seconds.")
                    time.sleep(sleep_time)
                    emails_sent = 0  # Reset the counter
                    start_time = time.time()  # Reset the timer

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject_template.replace("%NOMEHOTEL%", hotel_name)

            # Personalize the email body
            email_body = email_body_template.replace("%NOMEHOTEL%", hotel_name)
            message.attach(MIMEText(email_body, "html"))

            try:
                # Send email
                server.sendmail(sender_email, recipient_email, message.as_string())
                print(f"Email sent to {recipient_email}")
                emails_sent += 1

                # Update sent status to 1 in CSV file
                csvwriter.writerow([hotel_name, recipient_email, 'Sent'])

                # Random sleep between 5 to 10 seconds
                sleep_duration = random.uniform(5, 10)
                time.sleep(sleep_duration)
            except smtplib.SMTPRecipientsRefused as e:
                print(f"Failed to send email to {recipient_email}: {e}")
                csvwriter.writerow([hotel_name, recipient_email, 'Failed'])  # Record failure

    # Close SMTP session
    server.quit()

    print("Emails sent successfully!")

try:
    # Parse form data
    form = cgi.FieldStorage()

    # Debug: Print the received form data
    print("Content-type: text/plain\n")
    print("Received form data:")
    print(f"num_emails_to_send: {form.getvalue('num_emails_to_send')}")
    print(f"recipient_csv: {form['recipient_csv'].filename}")
    print(f"email_html: {form['email_html'].filename}")

    num_emails_to_send = int(form.getvalue("num_emails_to_send"))
    recipient_csv = form["recipient_csv"].file
    email_html = form["email_html"].file

    # Save uploaded files
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    recipient_csv_path = os.path.join('uploads', "recipient_list.csv")
    email_html_path = os.path.join('uploads', "email_template.html")

    with open(recipient_csv_path, "wb") as f:
        f.write(recipient_csv.read())

    with open(email_html_path, "wb") as f:
        f.write(email_html.read())

    send_emails(recipient_csv_path, email_html_path, num_emails_to_send)

    print("Content-type: text/plain\n")
    print("Emails are being sent.")
except Exception as e:
    print("Content-type: text/plain\n")
    print(f"An error occurred: {e}")
