import smtplib
from email.mime.text import MIMEText
import sqlite3
import time


class EmailActions:
    def fetch_contacts_from_database(self):
        connection = sqlite3.connect('newContacts.db')
        cursor = connection.cursor()
        cursor.execute("SELECT firstname, lastname, email FROM contacts")
        contacts = cursor.fetchall()
        connection.close()
        return contacts

    def send_email(self, subject, body, sender, recipient, password):
        if recipient is None:
            print("Recipient email address is not provided.")
            return

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipient, msg.as_string())
                print("Message sent to", recipient)
        except Exception as e:
            print("An error occurred while sending the email:", e)

    def send_emails_and_clear_database(self):
        subject = "Welcome"
        body_template = "Dear {},\nThanks for using MyCelium.\n\nGG WP,\nMyCelium"
        sender = "email@example.com"
        password = "pas s wor d"

        #fetch contacts from the database
        contacts = self.fetch_contacts_from_database()

        #Send personalized emails and update recipient's email
        for contact in contacts:
            first_name, last_name, email = contact
            recipient_body = body_template.format(first_name)
            self.send_email(subject, recipient_body, sender, email, password)

        #Clear the SQLite database
        connection = sqlite3.connect('newContacts.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM contacts")
        connection.commit()
        connection.close()

email_actions = EmailActions()

def loop():
#Run the loop every 15 seconds
    while True:
        email_actions.send_emails_and_clear_database()
        time.sleep(15)  #Timer
