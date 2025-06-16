import os
import requests

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "you@example.com")  # fallback if not set

def send_mailgun_email_with_attachment():
    if not MAILGUN_DOMAIN or not MAILGUN_API_KEY or not ALERT_EMAIL:
        print("❌ Mailgun config is missing.")
        return

    with open("bourbon_report.pdf", "rb") as pdf_file:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            files=[("attachment", ("bourbon_report.pdf", pdf_file.read()))],
            data={
                "from": f"Bourbon Pourcast <mailgun@{MAILGUN_DOMAIN}>",
                "to": [ALERT_EMAIL],
                "subject": "Your Daily Bourbon Pourcast Report",
                "text": "Attached is your daily bourbon search results PDF from Pourcast.",
            },
        )

    if response.status_code == 200:
        print("✅ Email with PDF sent successfully.")
    else:
        print(f"❌ Failed to send email: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    send_mailgun_email_with_attachment()
