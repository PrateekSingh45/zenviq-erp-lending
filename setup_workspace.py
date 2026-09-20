import os, frappe, json

os.chdir("sites")
frappe.init(site="zenviq.localhost", sites_path=".")
frappe.connect()

ws_name = "ZENVIQ Lending"

shortcuts = [
    {"type": "Page", "link_to": "owner-cockpit", "label": "👑 CEO / Owner Cockpit", "color": "Indigo"},
    {"type": "DocType", "link_to": "Lending Lead", "label": "Lending Leads"},
    {"type": "DocType", "link_to": "Borrower Profile", "label": "Borrower Profiles"},
    {"type": "DocType", "link_to": "KYC Verification", "label": "KYC Verifications"},
    {"type": "DocType", "link_to": "Credit Assessment", "label": "Credit Assessments"},
    {"type": "DocType", "link_to": "Loan Application", "label": "Loan Applications"},
    {"type": "DocType", "link_to": "eSign Request", "label": "eSign Requests"},
    {"type": "DocType", "link_to": "Loan", "label": "Loans"},
    {"type": "DocType", "link_to": "Loan Repayment", "label": "Loan Repayments"},
    {"type": "DocType", "link_to": "Collection Task", "label": "Collection Tasks"},
    {"type": "DocType", "link_to": "Loan Closure Request", "label": "Loan Closures & NOC"},
    {"type": "Report", "link_to": "Loan Portfolio Summary", "label": "Portfolio Summary Report"},
    {"type": "Report", "link_to": "DPD Aging Analysis", "label": "DPD Aging Report"}
]

links = [
    {"label": "Executive & Management", "type": "Card Break", "icon": "briefcase"},
    {"label": "👑 CEO / Owner Cockpit", "type": "Link", "link_type": "Page", "link_to": "owner-cockpit"},
    {"label": "Loan Portfolio Summary", "type": "Link", "link_type": "Report", "link_to": "Loan Portfolio Summary"},
    {"label": "DPD Aging Analysis", "type": "Link", "link_type": "Report", "link_to": "DPD Aging Analysis"},

    {"label": "Borrower Onboarding", "type": "Card Break", "icon": "user"},
    {"label": "Lending Leads", "type": "Link", "link_type": "DocType", "link_to": "Lending Lead"},
    {"label": "Borrower Profiles", "type": "Link", "link_type": "DocType", "link_to": "Borrower Profile"},
    {"label": "KYC Verifications (eKYC/PAN)", "type": "Link", "link_type": "DocType", "link_to": "KYC Verification"},
    
    {"label": "Underwriting & Approval", "type": "Card Break", "icon": "file-text"},
    {"label": "Credit Assessments (CIBIL)", "type": "Link", "link_type": "DocType", "link_to": "Credit Assessment"},
    {"label": "Loan Applications", "type": "Link", "link_type": "DocType", "link_to": "Loan Application"},
    {"label": "eSign Requests (Aadhaar eSign)", "type": "Link", "link_type": "DocType", "link_to": "eSign Request"},

    {"label": "Loan Servicing & Accounting", "type": "Card Break", "icon": "credit-card"},
    {"label": "All Loans", "type": "Link", "link_type": "DocType", "link_to": "Loan"},
    {"label": "Loan Disbursements", "type": "Link", "link_type": "DocType", "link_to": "Loan Disbursement"},
    {"label": "Loan Repayments", "type": "Link", "link_type": "DocType", "link_to": "Loan Repayment"},
    {"label": "Loan Products (Master)", "type": "Link", "link_type": "DocType", "link_to": "Loan Product"},

    {"label": "Collections & Closures", "type": "Card Break", "icon": "alert-circle"},
    {"label": "Collection Tasks (DPD)", "type": "Link", "link_type": "DocType", "link_to": "Collection Task"},
    {"label": "Loan Closure & NOC", "type": "Link", "link_type": "DocType", "link_to": "Loan Closure Request"},

    {"label": "Lending Intelligence Reports", "type": "Card Break", "icon": "bar-chart-2"},
    {"label": "EMI Collection Report", "type": "Link", "link_type": "Report", "link_to": "EMI Collection Report"},
    {"label": "Disbursement Register", "type": "Link", "link_type": "Report", "link_to": "Disbursement Register"},
    {"label": "NPA and Recovery Report", "type": "Link", "link_type": "Report", "link_to": "NPA and Recovery Report"},
    {"label": "Borrower 360 Ledger", "type": "Link", "link_type": "Report", "link_to": "Borrower 360 Ledger"}
]

card_names = [
    "Total Active Loans",
    "Verified Borrowers",
    "Active Overdue Cases",
    "Total Disbursed"
]

content_blocks = [
    {"type": "header", "data": {"text": "ZENVIQ Individual Lending Management", "level": 3}},
    {"type": "paragraph", "data": {"text": "Digital Lending Suite for Individual Borrowers: Lead → eKYC → Underwriting → eSign → Disbursement → Collections → NOC Closure."}},
]

for c in card_names:
    content_blocks.append({"type": "card", "data": {"card_name": c}})

for sc in shortcuts:
    content_blocks.append({"type": "shortcut", "data": {"shortcut_name": sc["label"]}})

if frappe.db.exists("Workspace", ws_name):
    frappe.delete_doc("Workspace", ws_name, ignore_permissions=True)
    frappe.db.commit()

ws = frappe.new_doc("Workspace")
ws.name = ws_name
ws.label = ws_name
ws.title = ws_name
ws.icon = "credit-card"
ws.module = "ZENVIQ Lending"
ws.public = 1
ws.sequence_id = 1
ws.content = json.dumps(content_blocks)

for sc in shortcuts:
    ws.append("shortcuts", sc)
    
for lk in links:
    ws.append("links", lk)
    
for c in card_names:
    ws.append("number_cards", {"number_card_name": c})

ws.insert(ignore_permissions=True)
frappe.db.commit()

print(f"Workspace '{ws_name}' successfully updated with Owner Cockpit link!")
frappe.destroy()
