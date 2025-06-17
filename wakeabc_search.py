import requests
from bs4 import BeautifulSoup
import pdfkit
from datetime import datetime

# Define the bourbon search terms
SEARCH_TERMS = [
    "blanton", "eh taylor", "george t stagg", "weller", "van winkle",
    "elmer t lee", "booker", "stagg", "michter", "angels envy", "1792",
    "four roses", "blue note", "bardstown", "old forester", "woodford"
]

BASE_URL = "https://www.wakeabc.com"
SEARCH_URL = f"{BASE_URL}/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"

def search_bourbon(term):
    response = requests.get(SEARCH_URL, params={"q": term}, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.select(".product-listing .item")

    if not results:
        return f"🔍 Searching for: {term}\n❌ No results found.\n"

    output = [f"🔍 Searching for: {term}"]
    for item in results:
        name = item.select_one(".item-title").get_text(strip=True)
        price = item.select_one(".price").get_text(strip=True)
        size = item.select_one(".item-size").get_text(strip=True) if item.select_one(".item-size") else "N/A"
        inventory_info = item.select(".store-inventory .store")

        output.append(f"- {name}\n  Price: {price} | Size: {size}")

        if inventory_info:
            output.append("  Locations:")
            for store in inventory_info:
                location = store.select_one(".store-address").get_text(" ", strip=True)
                quantity = store.select_one(".quantity").get_text(strip=True)
                output.append(f"    - {location}: {quantity} in stock")
        else:
            output.append("  Inventory: Not Available")

    output.append("")  # newline
    return "\n".join(output)

def save_txt(content):
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

def save_html(content):
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(f"<pre>{content}</pre>")

def save_pdf():
    pdfkit.from_file(HTML_OUTPUT, PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")
    results = [f"Bourbon Pourcast Search Results\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
    results.append(f"Search Terms: {', '.join(SEARCH_TERMS)}\n")

    for term in SEARCH_TERMS:
        results.append(search_bourbon(term))

    final_output = "\n".join(results)
    save_txt(final_output)
    save_html(final_output)
    save_pdf()
    print("✅ All searches complete. Results saved to:")
    print(f"- {TXT_OUTPUT}")
    print(f"- {HTML_OUTPUT}")
    print(f"- {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
