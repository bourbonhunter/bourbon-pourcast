import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

def send_bourbon_email():
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    to_email = os.getenv("ALERT_EMAIL", "your@email.com")  # Update with your test email or use a GitHub Secret
    from_email = "alerts@bourbonpourcast.com"  # Change to a verified sender from your SendGrid account

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject="🥃 New Bourbon Pourcast Results Available",
        html_content="""
        <p>Hello Bourbon Hunter,</p>
        <p>Your latest search results are ready!</p>
        <ul>
            <li><a href="https://github.com/bourbonhunter/bourbon-pourcast/raw/main/search_results.html">View HTML Report</a></li>
            <li><a href="https://github.com/bourbonhunter/bourbon-pourcast/raw/main/bourbon_report.pdf">Download PDF Report</a></li>
        </ul>
        <p>Cheers,<br>Bourbon Pourcast</p>
        """
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print("✅ Email sent:", response.status_code)
    except Exception as e:
        print("❌ Failed to send email:", e)

if __name__ == "__main__":
    send_bourbon_email()
