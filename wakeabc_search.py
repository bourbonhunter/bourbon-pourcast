from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
import os
from datetime import datetime
import pdfkit
import requests

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")

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
    body {
      background-color: #FAF3E0;
      color: #333;
      font-family: Arial, sans-serif;
      font-size: 20px;
      padding: 20px;
    }
    h1, h2 {
      color: #7B3F00;
    }
    .date {
      font-style: italic;
      color: #A97448;
      margin-bottom: 20px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 30px;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 8px 12px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background-color: #e2cdb6;
      color: #5A2600;
    }
    ul {
      margin: 0;
      padding-left: 18px;
    }
    li {
      margin-bottom: 4px;
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Pour Decisions Pourcast</h1>
      <p class="date"><em>June 19, 2025</em></p>
    </div>
    <img src="logo.png" alt="Pour Decisions Logo" style="height: 120px; margin-left: 40px; border-radius: 6px;" />
  </header>
""")

for term in search_terms:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        print(f"🔍 Searching for: {term}")
        driver.get("https://wakeabc.com/search-results/")
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "productSearch"))
        )
        search_input.clear()
        search_input.send_keys(term)
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "wake-product"))
        )
        time.sleep(2)

        product_elements = driver.find_elements(By.CLASS_NAME, "wake-product")

        with open(output_txt, "a", encoding="utf-8") as txt, open(output_html, "a", encoding="utf-8") as html:
            txt.write(f"Results for '{term}':\n")
            html.write(f"<h2>Results for '{term}':</h2>\n<table>\n<tr><th>Name</th><th>Price</th><th>Size</th><th>Stores</th></tr>\n")

            if not product_elements:
                txt.write("No results found.\n\n")
                html.write("<tr><td colspan='4'>No results found.</td></tr>\n</table><hr>\n")
                continue

            for product in product_elements:
                try:
                    title = product.find_element(By.TAG_NAME, "h4").text.strip()
                except:
                    title = "Unknown Title"

                try:
                    price = product.find_element(By.CLASS_NAME, "price").text.strip()
                except:
                    price = "Price not listed"

                try:
                    size = product.find_element(By.CLASS_NAME, "size").text.strip()
                except:
                    size = "Size not listed"

                result_txt = f"- {title}\n  Price: {price} | Size: {size}\n"
                stores_html = ""

                try:
                    show_btn = product.find_element(By.CLASS_NAME, "collapse-heading")
                    driver.execute_script("arguments[0].click();", show_btn)
                    time.sleep(0.5)

                    inventory_div = product.find_element(By.CLASS_NAME, "inventory-collapse")
                    store_items = inventory_div.find_elements(By.TAG_NAME, "li")

                    if store_items:
                        result_txt += "  Locations:\n"
                        stores_html += "<ul>"
                        for store in store_items:
                            try:
                                addr = store.find_element(By.CLASS_NAME, "address").get_attribute("innerHTML").strip().replace("<br>", ", ")
                                qty = store.find_element(By.CLASS_NAME, "quantity").text.strip()
                                result_txt += f"    - {addr}: {qty}\n"
                                maps_link = f"https://www.google.com/maps/search/?api=1&query={addr.replace(' ', '+')}"
                                stores_html += f"<li><a href='{maps_link}' target='_blank'>{addr}</a> — {qty}</li>"
                            except:
                                continue
                        stores_html += "</ul>"
                except:
                    result_txt += "  Inventory: Not Available\n"
                    stores_html = "Not Available"

                html.write(f"<tr><td><strong>{title}</strong></td><td>{price}</td><td>{size}</td><td>{stores_html}</td></tr>\n")
                txt.write(result_txt + "\n")

            txt.write("-" * 40 + "\n\n")
            html.write("</table><hr>\n")

    except Exception:
        print("\n❌ Error encountered:")
        traceback.print_exc()
    finally:
        driver.quit()

with open(output_html, "a", encoding="utf-8") as f:
    f.write("</body></html>")

try:
    pdfkit.from_file(output_html, output_pdf, configuration=pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf"))
except Exception as e:
    print(f"❌ PDF generation failed: {e}")

def send_email_with_attachment(pdf_path):
    if not (MAILGUN_DOMAIN and MAILGUN_API_KEY and ALERT_EMAIL):
        raise EnvironmentError("Missing one or more Mailgun environment variables.")
    with open(pdf_path, "rb") as pdf_file:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            files=[("attachment", ("bourbon_report.pdf", pdf_file.read()))],
            data={
                "from": f"Pourcast <mailgun@{MAILGUN_DOMAIN}>",
                "to": [ALERT_EMAIL],
                "subject": "Pour Decisions Pourcast PDF Report",
                "text": "Attached is your bourbon search report."
            },
        )
    if response.status_code == 200:
        print("✅ Email sent successfully.")
    else:
        print(f"❌ Failed to send email: {response.status_code}\n{response.text}")

send_email_with_attachment(output_pdf)
