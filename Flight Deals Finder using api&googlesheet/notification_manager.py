# TWILIO SMS API
import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib
from email.message import EmailMessage


load_dotenv("config.env.txt")
api_key = os.getenv("RAIN_API_KEY")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

my_email = "spenzr2@gmail.com"
password = "linbeqtabbhzplil"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def send_sms(self, body):
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=body,
            to='whatsapp:+971553790065'
        )
        print(message.sid)

    def send_emails(self, body, customer_emails):
        msg = EmailMessage()
        msg["Subject"] = f" Low Price Flight Deal Available"
        msg.set_content(body)
        for emails in customer_emails:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=my_email, to_addrs=emails, msg=msg.as_string())
