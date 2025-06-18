
import os
import time
import pdfkit
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_TERMS = ["blanton", "old fitz", "eagle rare", "taylor", "weller", "stagg", "elmer"]
BASE_URL = "https://wakeabc.com/search-our-inventory/"

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def perform_search(term, driver):
    driver.get(BASE_URL)
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "s"))
        )
        input_box.clear()
        input_box.send_keys(term)
        input_box.submit()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".elementor-post"))
        )

        time.sleep(2)
        posts = driver.find_elements(By.CSS_SELECTOR, ".elementor-post")
        results = []

        for post in posts:
            title = post.find_element(By.CSS_SELECTOR, ".elementor-post__title").text.strip()
            try:
                button = post.find_element(By.XPATH, ".//button[contains(text(), 'Show Inventory')]")
                driver.execute_script("arguments[0].click();", button)
                WebDriverWait(post, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "store-inventory"))
                )
                inventory = post.find_element(By.CLASS_NAME, "store-inventory").text.strip()
            except:
                inventory = "Inventory: Not Available"

            results.append(f"<li><strong>{title}</strong><br>{inventory}</li>")

        if results:
            return f"<h3>🔍 Searching for: {term}</h3><ul>{''.join(results)}</ul>"
        else:
            return f"<h3>🔍 Searching for: {term}</h3><p>❌ No results found.</p>"

    except Exception as e:
        return f"<h3>🔍 Searching for: {term}</h3><p>⚠️ Error encountered: {e}</p>"

def generate_html(results):
    with open("template.html", "r", encoding="utf-8") as f:
        template = Template(f.read())
    return template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        search_blocks=results
    )

def save_files():
    driver = setup_driver()
    results = []
    for term in SEARCH_TERMS:
        print(f"Searching for: {term}")
        results.append(perform_search(term, driver))
    driver.quit()

    html_content = generate_html(results)

    with open("search_results.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open("search_results.txt", "w", encoding="utf-8") as f:
        f.write(BeautifulSoup(html_content, "html.parser").get_text())
    pdfkit.from_file("search_results.html", "bourbon_report.pdf")

def main():
    print("🔍 Running bourbon inventory search...")
    save_files()
    print("✅ All reports saved successfully.")

if __name__ == "__main__":
    main()
