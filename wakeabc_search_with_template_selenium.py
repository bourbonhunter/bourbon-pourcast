
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pdfkit
from jinja2 import Template

SEARCH_TERMS = [
    "blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"
]

BASE_URL = "https://wakeabc.com/search-our-inventory/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_inventory():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    results = []
    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        driver.get(f"{BASE_URL}?s={term}")
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        listings = soup.select(".elementor-post")

        if listings:
            term_block = {
                "term": term,
                "items": []
            }
            for item in listings:
                title = item.select_one(".elementor-post__title")
                location = item.select_one(".elementor-post__excerpt")
                if title and location:
                    term_block["items"].append({
                        "title": title.text.strip(),
                        "location": location.text.strip()
                    })
            results.append(term_block)
        else:
            results.append({
                "term": term,
                "items": []
            })

    driver.quit()
    return results

def generate_html(results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())

    html = template.render(timestamp=timestamp, results=results)
    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(html)
    return html

def save_files():
    results = fetch_inventory()
    html_content = generate_html(results)

    with open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(BeautifulSoup(html_content, "html.parser").get_text())

    pdfkit.from_file("search_results.html", "bourbon_report.pdf")

def main():
    print("🔍 Running bourbon inventory search...")
    save_files()
    print("✅ All done!")

if __name__ == "__main__":
    main()
