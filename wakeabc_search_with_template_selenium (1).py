import time
import pdfkit
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

SEARCH_TERMS = ["blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"]
BASE_URL = "https://wakeabc.com/search-our-inventory/"

def fetch_inventory():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    results = []

    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        driver.get(f"{BASE_URL}?s={term}")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.select(".elementor-post")

        if listings:
            results.append(f"<h3>🔍 Searching for: {term}</h3><ul>")
            for item in listings:
                title = item.select_one(".elementor-post__title")
                location = item.select_one(".elementor-post__excerpt")
                if title and location:
                    results.append(f"<li><strong>{title.text.strip()}</strong><br>{location.text.strip()}</li>")
            results.append("</ul>")
        else:
            results.append(f"<h3>🔍 Searching for: {term}</h3><p>❌ No results found.</p>")

    driver.quit()
    return results

def generate_html(results):
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()
    content = "\n".join(results)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return template.replace("{{timestamp}}", timestamp).replace("{{results}}", content)

def save_files():
    results = fetch_inventory()
    html_content = generate_html(results)

    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(BeautifulSoup(html_content, "html.parser").get_text())

    pdfkit.from_file("search_results.html", "bourbon_report.pdf")

def main():
    print("🔍 Running bourbon inventory search...")
    save_files()
    print("✅ Search completed and files saved.")

if __name__ == "__main__":
    main()