import os
import requests

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def send_email_with_attachment(pdf_file_path):
    if not all([MAILGUN_DOMAIN, MAILGUN_API_KEY, RECIPIENT_EMAIL]):
        raise EnvironmentError("Missing one or more Mailgun environment variables.")

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        files=[("attachment", open(pdf_file_path, "rb"))],
        data={
            "from": f"Bourbon Pourcast <mailgun@{MAILGUN_DOMAIN}>",
            "to": [RECIPIENT_EMAIL],
            "subject": "Pour Decisions Pourcast Report",
            "text": "Attached is your latest Bourbon Pourcast inventory report."
        }
    )