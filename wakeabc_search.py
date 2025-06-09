
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

search_terms = ["Old Fitz", "Blanton", "Eagle Rare", "stagg", "Van Winkle", "king of kentucky", "parkers", "elmer", "taylor", "weller", "old forester", "michter", "blue note"]

output_txt = "search_results.txt"
output_html = "search_results.html"
output_pdf = "bourbon_report.pdf"
today = datetime.now().strftime("%B %d, %Y")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

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
      font-size: 28px;
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
    <img src="logo.png" alt="Logo" style="height: 300px; margin-left: 40px;" />
  </header>
""")

for term in search_terms:
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"🔍 Searching for: {term}")
        driver.get("https://wakeabc.com/search-results/")

        try:
            search_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.NAME, "productSearch"))
            )
            search_input.clear()
            search_input.send_keys(term)
            search_input.send_keys(Keys.RETURN)
        except:
            print(f"❌ Search input not found for {term}")
            continue

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "wake-product"))
            )
        except:
            print(f"❌ Timeout waiting for products for {term}")
            continue

        time.sleep(2)

        product_elements = driver.find_elements(By.CLASS_NAME, "wake-product")

        with open(output_txt, "a", encoding="utf-8") as txt, open(output_html, "a", encoding="utf-8") as html:
            txt.write(f"Results for '{term}':\n")
            html.write(f"<h2>Results for '{term}':</h2>\n<table>\n<tr><th>Name</th><th>Price</th><th>Size</th><th>Stores</th></tr>\n")

            if not product_elements:
                txt.write("No results found.\n\n")
                html.write("<tr><td colspan='4'>No results found.</td></tr>\n</table><hr>\n")
            else:
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

                    result_html = f"<tr><td><strong>{title}</strong></td><td>{price}</td><td>{size}</td><td>{stores_html}</td></tr>\n"

                    print(result_txt)
                    txt.write(result_txt + "\n")
                    html.write(result_html)

                txt.write("-" * 40 + "\n\n")
                html.write("</table><hr>\n")

    except Exception:
        print("\n❌ Error encountered:")
        traceback.print_exc()
    finally:
        driver.quit()

with open(output_html, "a", encoding="utf-8") as f:
    f.write("</body></html>")

print(f"\n✅ All searches complete. Results saved to:\n- {output_txt}\n- {output_html}")

options = {
    'enable-local-file-access': '',
    'disable-external-links': '',
    'disable-smart-shrinking': ''
}

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
pdfkit.from_file(output_html, output_pdf, configuration=config, options=options)
