from requests import Response,post,request
from typing import List
import os
#pip install python-dotenc ....values stored in .env file
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

class MailGunException(Exception):

    def __init__(self,msg):
        super().__init__(msg)

def send_email_confirmation(to:List,subject:str,mail_body:str):

    if MAILGUN_DOMAIN is None:
        raise MailGunException("Mailgun domain could not be loaded")
    if MAILGUN_API_KEY is None:
        raise MailGunException("Mailgun API key could not be loaded")

    resp = post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"Mailgun User <mailgun@{MAILGUN_DOMAIN}>",
              "to": to,
              "subject": subject,
              "html": mail_body})

    if resp.status_code != 200:
        raise MailGunException("Registration email could not be sent")

    return resp