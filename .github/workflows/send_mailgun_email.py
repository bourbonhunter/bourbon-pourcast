import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

def send_test_email():
    if not all([MAILGUN_API_KEY, MAILGUN_DOMAIN, ALERT_EMAIL]):
        print("❌ Missing one or more required environment variables.")
        return

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Bourbon Pourcast <mailgun@{MAILGUN_DOMAIN}>",
            "to": ALERT_EMAIL,
            "subject": "Test Bourbon Pourcast Alert",
            "text": "This is a test alert from your Bourbon Pourcast app using Mailgun."
        }
    )

    if response.status_code == 200:
        print("✅ Email sent successfully!")
    else:
        print(f"❌ Failed to send email. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    send_test_email()
