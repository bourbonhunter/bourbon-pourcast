import os
import csv
from datetime import datetime
from fpdf import FPDF

CSV_CURRENT = "current_inventory.csv"
CSV_PREVIOUS = "previous_inventory.csv"
TXT_OUTPUT = "search_results.txt"
HTML_OUTPUT = "search_results.html"
PDF_OUTPUT = "bourbon_report.pdf"
FONT_PATH = "DejaVuSans.ttf"
FONT_NAME = "DejaVu"

def simulate_bourbon_inventory():
    now = datetime.now().second
    if now % 2 == 0:
        return [
            {"name": "Blanton's", "store": "Cary", "qty": 12},
            {"name": "Eagle Rare", "store": "Raleigh", "qty": 8},
            {"name": "Weller Special Reserve", "store": "Durham", "qty": 6},
        ]
    else:
        return [
            {"name": "Eagle Rare", "store": "Raleigh", "qty": 6},
            {"name": "Weller Special Reserve", "store": "Durham", "qty": 5},
            {"name": "Old Forester 1920", "store": "Garner", "qty": 2},
        ]

def save_inventory_csv(filename, inventory):
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "store", "qty"])
        writer.writeheader()
        writer.writerows(inventory)

def load_inventory_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def compare_inventory(current, previous):
    current_set = {(item["name"], item["store"]) for item in current}
    previous_set = {(item["name"], item["store"]) for item in previous}

    added = current_set - previous_set
    removed = previous_set - current_set

    return added, removed

def format_inventory_text(inventory):
    lines = []
    for item in inventory:
        lines.append(f'{item["name"]} - {item["store"]} ({item["qty"]} in stock)')
    return "\n".join(lines)

def save_txt(filename, delta_text, inventory_text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("📈 Pour Decisions Pourcast\n")
        f.write("=" * 40 + "\n\n")
        f.write(delta_text + "\n\n")
        f.write(inventory_text)

def save_html(filename, delta_text, inventory_text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
  <title>Pour Decisions Pourcast</title>
  <style>
    body {{ font-family: Arial, sans-serif; padding: 2em; background: #fffdf9; color: #333; }}
    h1 {{ color: #7B3F00; }}
    pre {{ white-space: pre-wrap; font-family: monospace; }}
  </style>
</head>
<body>
  <h1>Pour Decisions Pourcast</h1>
  <p><em>{datetime.now().strftime("%B %d, %Y")}</em></p>
  <pre>{delta_text}</pre>
  <hr>
  <pre>{inventory_text}</pre>
</body>
</html>""")

def save_pdf(delta_text, inventory_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(FONT_NAME, '', FONT_PATH, uni=True)
    pdf.set_font(FONT_NAME, '', 12)
    pdf.multi_cell(0, 10, "📈 Pour Decisions Pourcast\n\n" + delta_text + "\n\n" + inventory_text)
    pdf.output(PDF_OUTPUT)

def main():
    print("🔍 Running bourbon inventory search...")

    current_inventory = simulate_bourbon_inventory()
    save_inventory_csv(CSV_CURRENT, current_inventory)

    previous_inventory = load_inventory_csv(CSV_PREVIOUS)

    added, removed = compare_inventory(current_inventory, previous_inventory)

    delta_text = "🔼 Added Items:\n" + (
        "\n".join([f"{name} - {store}" for name, store in added]) if added else "None"
    )
    delta_text += "\n\n🔽 Removed Items:\n" + (
        "\n".join([f"{name} - {store}" for name, store in removed]) if removed else "None"
    )

    inventory_text = format_inventory_text(current_inventory)

    save_txt(TXT_OUTPUT, delta_text, inventory_text)
    save_html(HTML_OUTPUT, delta_text, inventory_text)
    save_pdf(delta_text, inventory_text)

    os.replace(CSV_CURRENT, CSV_PREVIOUS)
    print(f"\n✅ All outputs saved: {TXT_OUTPUT}, {HTML_OUTPUT}, {PDF_OUTPUT}")

if __name__ == "__main__":
    main()
