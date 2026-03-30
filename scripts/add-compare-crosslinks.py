#!/usr/bin/env python3
"""Add 'Related Compare Tools' cross-link boxes to guides that are missing them."""
import os, re

GUIDES_DIR = "/home/ec2-user/sorted-my/guides"

# Mapping: guide → list of (compare_slug, link_text)
GUIDE_COMPARE_MAP = {
    # Guides with 0 compare links
    "police-report": [
        ("car-insurance", "Compare car insurance plans"),
    ],
    "contractor-went-dark": [
        ("home-insurance", "Compare home insurance plans"),
    ],
    "getting-married-muslim": [
        ("life-insurance", "Compare life insurance plans"),
        ("medical-insurance", "Compare medical insurance plans"),
        ("savings-account", "Compare savings account rates"),
    ],
    "getting-married-non-muslim": [
        ("life-insurance", "Compare life insurance plans"),
        ("medical-insurance", "Compare medical insurance plans"),
        ("savings-account", "Compare savings account rates"),
    ],
    "registering-death": [
        ("life-insurance", "Compare life insurance plans"),
        ("takaful-vs-conventional", "Takaful vs conventional insurance"),
    ],
    "registering-newborn": [
        ("life-insurance", "Compare life insurance plans"),
        ("medical-insurance", "Compare medical insurance plans"),
        ("savings-account", "Compare savings account rates"),
    ],
    "transferring-car-ownership": [
        ("car-insurance", "Compare car insurance plans"),
        ("car-loan", "Compare car loan rates"),
    ],
    "applying-pr-mm2h": [
        ("savings-account", "Compare savings account rates"),
        ("fixed-deposit", "Compare fixed deposit rates"),
    ],
    "kwsp-i-akaun": [
        ("fixed-deposit", "Compare fixed deposit rates"),
        ("unit-trust", "Compare unit trust funds"),
        ("savings-account", "Compare savings account rates"),
    ],
    "claiming-maternity-leave": [
        ("medical-insurance", "Compare medical insurance plans"),
        ("life-insurance", "Compare life insurance plans"),
    ],
    # Guides with 1 link — add more relevant ones
    "akpk-debt-management": [
        ("personal-loan", "Compare personal loan rates"),
        ("credit-card", "Compare credit cards"),
    ],
    "claiming-income-tax-refund": [
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "mydeposit-guide": [
        ("home-loan", "Compare home loan rates"),
        ("home-insurance", "Compare home insurance plans"),
    ],
    "renting-out-room": [
        ("rental-yield", "Rental yield calculator"),
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "missed-ptptn-payment": [
        ("ptptn-calculator", "PTPTN repayment calculator"),
    ],
    "sspn-i-guide": [
        ("ptptn-calculator", "PTPTN repayment calculator"),
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "car-accident-guide": [
        ("car-insurance", "Compare car insurance plans"),
    ],
    "getting-driving-license": [
        ("car-insurance", "Compare car insurance plans"),
        ("car-loan", "Compare car loan rates"),
    ],
    "getting-motorcycle-license": [
        ("car-insurance", "Compare vehicle insurance plans"),
    ],
    "freelancer-invoicing": [
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "kwsp-akaun-fleksibel-withdrawal": [
        ("fixed-deposit", "Compare fixed deposit rates"),
        ("savings-account", "Compare savings account rates"),
    ],
    "tng-ewallet": [
        ("ewallet", "Compare e-wallets in Malaysia"),
    ],
    "renewing-tenancy-agreement": [
        ("rental-yield", "Rental yield calculator"),
    ],
    "renting-first-apartment": [
        ("rental-yield", "Rental yield calculator"),
    ],
    "mysalam-guide": [
        ("medical-insurance", "Compare medical insurance plans"),
    ],
    "peka-b40": [
        ("medical-insurance", "Compare medical insurance plans"),
    ],
    "reading-ea-form": [
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "registering-enterprise": [
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "starting-sdn-bhd": [
        ("tax-calculator", "Malaysian tax calculator"),
    ],
    "hiring-first-employee": [
        ("tax-calculator", "Malaysian tax calculator"),
    ],
}

COMPARE_TOOL_BOX = """
<div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;margin:2rem 0">
  <p style="font-weight:600;color:#6c63ff;margin-bottom:0.5rem">Related Compare Tools</p>
  <p style="color:#8892b0;font-size:0.95rem">Find the best rates and compare options:</p>
  <ul style="margin-top:0.5rem">
{links}
  </ul>
</div>
"""

def build_links_html(compare_items):
    lines = []
    for slug, text in compare_items:
        lines.append(f'    <li><a href="../../compare/{slug}/">{text}</a></li>')
    return "\n".join(lines)

def already_has_compare_box(html):
    return "Related Compare Tools" in html

def insert_compare_box(html, box_html):
    # Insert before <footer> tag
    match = re.search(r'\n<footer>', html)
    if match:
        pos = match.start()
        return html[:pos] + "\n" + box_html + html[pos:]
    return None

updated = 0
skipped_existing = 0
skipped_no_match = 0

for guide_name, compare_items in GUIDE_COMPARE_MAP.items():
    guide_path = os.path.join(GUIDES_DIR, guide_name, "index.html")
    if not os.path.exists(guide_path):
        print(f"  SKIP (not found): {guide_name}")
        continue

    with open(guide_path, "r") as f:
        html = f.read()

    # Filter out compare tools already linked
    existing_links = re.findall(r'compare/([^/"]+)/', html)
    new_items = [(s, t) for s, t in compare_items if s not in existing_links]

    if not new_items:
        skipped_existing += 1
        continue

    if already_has_compare_box(html):
        # Append to existing box's <ul>
        ul_end = html.rfind("</ul>", html.index("Related Compare Tools"))
        if ul_end >= 0:
            new_links = "\n" + build_links_html(new_items)
            html = html[:ul_end] + new_links + "\n  " + html[ul_end:]
            with open(guide_path, "w") as f:
                f.write(html)
            updated += 1
            print(f"  APPENDED: {guide_name} (+{len(new_items)} links)")
    else:
        # Insert new box
        links_html = build_links_html(new_items)
        box = COMPARE_TOOL_BOX.format(links=links_html)
        result = insert_compare_box(html, box)
        if result:
            with open(guide_path, "w") as f:
                f.write(result)
            updated += 1
            print(f"  INSERTED: {guide_name} (+{len(new_items)} links)")
        else:
            print(f"  SKIP (no footer): {guide_name}")

print(f"\nDone: {updated} guides updated, {skipped_existing} already had all links")
