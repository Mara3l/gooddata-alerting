import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


class Notification:
    def __init__(self, email_send_from: str, email_send_to: str, email_server: str, email_password: str):
        self.email_send_from = email_send_from
        self.email_send_to = email_send_to
        self.email_server = email_server
        self.email_password = email_password

    def send_email(self, subject: str, text: str):
        msg = MIMEMultipart()
        msg["From"] = self.email_send_from
        msg["To"] = self.email_send_to
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = subject

        msg.attach(MIMEText(text))
        with smtplib.SMTP_SSL(self.email_server, 465) as smtp_server:
            smtp_server.login(self.email_send_from, self.email_password)
            smtp_server.sendmail(self.email_send_from, self.email_send_to, msg.as_string())
