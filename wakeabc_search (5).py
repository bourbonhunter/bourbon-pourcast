import os
import pdfkit
from datetime import datetime
from bs4 import BeautifulSoup
import requests

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "you@example.com")

search_terms = [
    "Old Fitz", "Blanton", "Eagle Rare", "stagg", "Van Winkle",
    "king of kentucky", "parkers", "elmer", "taylor", "weller",
    "old forester", "michter", "blue note"
]

output_txt = "search_results.txt"
output_html = "search_results.html"
output_pdf = "bourbon_report.pdf"
today = datetime.now().strftime("%B %d, %Y")

with open(output_txt, "w", encoding="utf-8") as f:
    f.write("Pour Decisions Pourcast\n" + "=" * 40 + "\n\n")

with open(output_html, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
  <title>Pour Decisions Pourcast</title>
  <style>
    body {{
      background-color: #FAF3E0;
      color: #333;
      font-family: Arial, sans-serif;
      font-size: 20px;
      padding: 20px;
    }}
    h1, h2 {{
      color: #7B3F00;
    }}
    .date {{
      font-style: italic;
      color: #A97448;
      margin-bottom: 20px;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 30px;
    }}
    th, td {{
      border: 1px solid #ccc;
      padding: 8px 12px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background-color: #e2cdb6;
      color: #5A2600;
    }}
    ul {{
      margin: 0;
      padding-left: 18px;
    }}
    li {{
      margin-bottom: 4px;
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Pour Decisions Pourcast</h1>
      <p class="date"><em>{today}</em></p>
    </div>
    <img src="logo.png" alt="Pour Decisions Logo" style="height: 120px; margin-left: 40px; border-radius: 6px;" />
  </header>
""")

for term in search_terms:
    print(f"🔍 Searching for: {term}")
    url = f"https://wakeabc.com/search-our-inventory/?s={term}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    matches = soup.select(".elementor-post")

    with open(output_txt, "a", encoding="utf-8") as txt, open(output_html, "a", encoding="utf-8") as html:
        txt.write(f"Results for '{term}':\n")
        html.write(f"<h2>Results for '{term}':</h2>\n<ul>")

        if not matches:
            txt.write("No results found.\n\n")
            html.write("<li>No results found.</li>\n</ul><hr>")
            continue

        for item in matches:
            title = item.select_one(".elementor-post__title")
            location = item.select_one(".elementor-post__excerpt")

            if title and location:
                name = title.get_text(strip=True)
                loc = location.get_text(strip=True)
                txt.write(f"- {name} ({loc})\n")
                html.write(f"<li><strong>{name}</strong>: {loc}</li>")

        txt.write("-" * 40 + "\n\n")
        html.write("</ul><hr>")

with open(output_html, "a", encoding="utf-8") as f:
    f.write("</body></html>")

try:
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdfkit.from_file(output_html, output_pdf, configuration=config)
except Exception as e:
    print(f"❌ PDF generation failed: {e}")

def send_email_with_attachment(filename):
    if not (MAILGUN_DOMAIN and MAILGUN_API_KEY and ALERT_EMAIL):
        raise EnvironmentError("Missing one or more Mailgun environment variables.")

    with open(filename, "rb") as pdf_file:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            files=[("attachment", (filename, pdf_file.read()))],
            data={
                "from": f"Bourbon Pourcast <mailgun@{MAILGUN_DOMAIN}>",
                "to": [ALERT_EMAIL],
                "subject": "Your Daily Bourbon Pourcast Report",
                "text": "Attached is your daily bourbon search results PDF from Pourcast.",
            },
        )
    if response.status_code == 200:
        print("✅ Email sent successfully.")
    else:
        print(f"❌ Failed to send email: {response.status_code}\n{response.text}")

send_email_with_attachment(output_pdf)
