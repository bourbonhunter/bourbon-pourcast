import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime

CSV_CURRENT = "current_inventory.csv"
CSV_PREVIOUS = "previous_inventory.csv"
TEXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"
FONT_NAME = "DejaVuSans"
FONT_FILE = "DejaVuSans.ttf"  # Make sure this is in the same directory

def run_inventory_search():
    # Placeholder for actual scraping logic — returns a sample DataFrame
    return pd.DataFrame([
        {"Product": "BLANTON'S SINGLE BARREL", "Store": "420 Woodburn Rd.", "Qty": 5},
        {"Product": "EAGLE RARE", "Store": "3615 SW Cary Parkway", "Qty": 12},
    ])

def save_csv(df, path):
    df.to_csv(path, index=False)

def generate_deltas(current_df, previous_df):
    added = pd.concat([current_df, previous_df, previous_df]).drop_duplicates(keep=False)
    removed = pd.concat([previous_df, current_df, current_df]).drop_duplicates(keep=False)
    return added, removed

def format_text_report(df):
    return "\n".join(f"{row['Product']} - {row['Store']} ({row['Qty']} in stock)" for _, row in df.iterrows())

def save_txt(content):
    with open(TEXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(content)

def save_html(content):
    html = f"<html><body><pre>{content}</pre></body></html>"
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(FONT_NAME, '', FONT_FILE, uni=True)
    pdf.set_font(FONT_NAME, size=10)
    pdf.multi_cell(0, 10, delta_text + "\n\n" + inventory_text)
    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")

    current_df = run_inventory_search()
    save_csv(current_df, CSV_CURRENT)

    if os.path.exists(CSV_PREVIOUS):
        previous_df = pd.read_csv(CSV_PREVIOUS)
        added, removed = generate_deltas(current_df, previous_df)
        delta_text = "📈 Items Added:\n" + format_text_report(added) + "\n\n📉 Items Removed:\n" + format_text_report(removed)
    else:
        delta_text = "🆕 First Run: No comparison available."

    inventory_text = format_text_report(current_df)

    full_text = delta_text + "\n\n============================\n\n" + inventory_text

    save_txt(full_text)
    save_html(full_text)
    save_pdf(delta_text, inventory_text)

    # Update previous with current
    os.replace(CSV_CURRENT, CSV_PREVIOUS)

    print("✅ All reports generated.")

if __name__ == "__main__":
    main()
