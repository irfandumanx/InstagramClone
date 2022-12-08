import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import Constants


class MailManager:

    def __init__(self):
        self.mail = Constants.MAIL_SENDER
        self.password = Constants.MAIL_PASSWORD
        self.mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        self.mailServer.ehlo()
        self.mailServer.starttls()
        self.mailServer.login(self.mail, self.password)

    def sendMailValidation(self, receiver, code):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Mail Degistirme Onayi"
        msg['From'] = self.mail
        msg['To'] = receiver
        html = """\
            <html>
              <head></head>
              <body>
                <a href="http://127.0.0.1:8080/mail-validation?code={}">Mail Onaylama Icin Tikla</a>
              </body>
            </html>
            """.format(code)
        msg.attach(MIMEText(html, 'html'))
        self.mailServer.sendmail(self.mail, receiver, msg.as_string())
