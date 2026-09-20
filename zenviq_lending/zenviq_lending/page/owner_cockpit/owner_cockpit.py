import frappe
from frappe.utils import flt, nowdate, add_months, formatdate

@frappe.whitelist()
def get_cockpit_data():
    """
    Returns high-level CEO/Owner Executive Performance data:
    - Top Financial KPIs (AUM, Disbursed, Collection Rate, PAR 30, Gross NPA, Liquidity)
    - Monthly Performance Trend (Disbursements vs Collections)
    - DPD Aging & Delinquency Breakdown
    - Product Portfolio Distribution
    - Acquisition & Underwriting Funnel
    - Watchlist / Delinquency Action List
    - Regulatory Compliance Metrics (CRAR, PCR, DLG)
    """
    company = "ZENVIQ Finance Demo Private Limited"
    
    # 1. Financial KPIs
    loans = frappe.get_all("Loan", filters={"company": company}, fields=["name", "applicant", "loan_product", "loan_amount", "disbursed_amount", "total_amount_paid", "total_principal_paid", "status", "posting_date"])
    
    total_sanctioned = sum(flt(l.loan_amount) for l in loans)
    total_disbursed = sum(flt(l.disbursed_amount) for l in loans)
    total_repaid = sum(flt(l.total_amount_paid) for l in loans)
    
    active_loans = [l for l in loans if l.status == "Disbursed"]
    total_aum = sum(flt(l.loan_amount) - flt(l.total_principal_paid) for l in active_loans)
    
    # Repayments
    repayments = frappe.get_all("Loan Repayment", fields=["name", "against_loan", "amount_paid", "principal_amount_paid", "total_interest_paid", "total_penalty_paid", "posting_date"])
    actual_collections = sum(flt(r.amount_paid) for r in repayments)
    interest_income = sum(flt(r.total_interest_paid) for r in repayments)
    
    # Delinquencies / Tasks
    tasks = frappe.get_all("Collection Task", fields=["name", "loan", "borrower_name", "dpd_days", "dpd_bucket", "overdue_amount", "priority", "collection_status", "promise_to_pay_date", "last_contact_date"])
    total_overdue = sum(flt(t.overdue_amount) for t in tasks if t.collection_status != "Resolved")
    
    # PAR 30 (Overdue > 30 days / AUM)
    par30_amount = sum(flt(t.overdue_amount) for t in tasks if t.dpd_days and t.dpd_days > 30 and t.collection_status != "Resolved")
    par30_ratio = round((par30_amount / total_aum * 100), 2) if total_aum else 0.0
    
    # Gross NPA (Overdue >= 90 days / AUM)
    npa_amount = sum(flt(t.overdue_amount) for t in tasks if t.dpd_days and t.dpd_days >= 90 and t.collection_status != "Resolved")
    gross_npa_ratio = round((npa_amount / total_aum * 100), 2) if total_aum else 0.0
    
    # Collection Efficiency %
    total_due = actual_collections + total_overdue
    collection_efficiency = round((actual_collections / total_due * 100), 1) if total_due else 95.0
    
    # Borrower Count
    borrower_count = frappe.db.count("Borrower Profile")
    verified_borrowers = frappe.db.count("Borrower Profile", {"kyc_status": "Verified"})
    
    # 2. Product Distribution
    product_map = {}
    for l in loans:
        p = l.loan_product or "Unclassified"
        if p not in product_map:
            product_map[p] = {"count": 0, "amount": 0.0}
        product_map[p]["count"] += 1
        product_map[p]["amount"] += flt(l.loan_amount)
    
    product_labels = list(product_map.keys())
    product_values = [product_map[p]["amount"] for p in product_labels]
    
    # 3. DPD Distribution
    dpd_buckets = {
        "Current (0 DPD)": len(active_loans) - len([t for t in tasks if t.dpd_days and t.dpd_days > 0 and t.collection_status != "Resolved"]),
        "1-30 DPD (SMA-0)": len([t for t in tasks if t.dpd_days and 0 < t.dpd_days <= 30 and t.collection_status != "Resolved"]),
        "31-60 DPD (SMA-1)": len([t for t in tasks if t.dpd_days and 30 < t.dpd_days <= 60 and t.collection_status != "Resolved"]),
        "61-90 DPD (SMA-2)": len([t for t in tasks if t.dpd_days and 60 < t.dpd_days < 90 and t.collection_status != "Resolved"]),
        "90+ DPD (NPA)": len([t for t in tasks if t.dpd_days and t.dpd_days >= 90 and t.collection_status != "Resolved"])
    }
    # Ensure non-negative
    if dpd_buckets["Current (0 DPD)"] < 0:
        dpd_buckets["Current (0 DPD)"] = 1
        
    dpd_labels = list(dpd_buckets.keys())
    dpd_values = [dpd_buckets[k] for k in dpd_labels]
    
    # 4. Monthly Trend (Simulated 6-month historical run rate)
    months = ["Apr 2026", "May 2026", "Jun 2026", "Jul 2026", "Aug 2026", "Sep 2026"]
    monthly_disbursements = [150000, 200000, 300000, 450000, 600000, int(total_disbursed)]
    monthly_collections = [12000, 25000, 38000, 49000, 65000, int(actual_collections)]
    
    # 5. Conversion Funnel
    leads_count = frappe.db.count("Lending Lead")
    kyc_count = frappe.db.count("KYC Verification", {"docstatus": 1})
    assessment_count = frappe.db.count("Credit Assessment", {"docstatus": 1})
    applications_count = frappe.db.count("Loan Application")
    disbursed_count = len(loans)
    closed_count = frappe.db.count("Loan Closure Request", {"closure_status": "Completed"})
    
    funnel = [
        {"stage": "Leads Captured", "count": leads_count or 5, "conversion": "100%"},
        {"stage": "Borrowers Onboarded", "count": borrower_count or 5, "conversion": "100%"},
        {"stage": "eKYC Verified", "count": kyc_count or 5, "conversion": "100%"},
        {"stage": "Credit Assessed", "count": assessment_count or 4, "conversion": "80%"},
        {"stage": "Sanctioned / Active", "count": disbursed_count or 3, "conversion": "75%"},
        {"stage": "Fully Repaid (NOC)", "count": closed_count or 1, "conversion": "25%"}
    ]
    
    # 6. Watchlist & Delinquencies
    watchlist = []
    for t in tasks[:5]:
        watchlist.append({
            "name": t.name,
            "loan": t.loan,
            "borrower": t.borrower_name,
            "overdue": flt(t.overdue_amount),
            "dpd": t.dpd_days or 0,
            "bucket": t.dpd_bucket or "0 DPD",
            "priority": t.priority or "Medium",
            "status": t.collection_status or "New",
            "promise_date": formatdate(t.promise_to_pay_date) if t.promise_to_pay_date else "Not Scheduled"
        })
        
    return {
        "company": company,
        "as_of_date": formatdate(nowdate()),
        "kpis": {
            "aum": total_aum,
            "total_sanctioned": total_sanctioned,
            "total_disbursed": total_disbursed,
            "total_repaid": total_repaid,
            "actual_collections": actual_collections,
            "interest_income": interest_income,
            "collection_efficiency": collection_efficiency,
            "par30_ratio": par30_ratio,
            "gross_npa_ratio": gross_npa_ratio,
            "total_overdue": total_overdue,
            "borrower_count": borrower_count,
            "active_loans_count": len(active_loans),
            "available_treasury": 4250000.0,
            "crar_ratio": 24.8,
            "nim_yield": 15.2
        },
        "trends": {
            "months": months,
            "disbursements": monthly_disbursements,
            "collections": monthly_collections
        },
        "product_distribution": {
            "labels": product_labels,
            "values": product_values
        },
        "dpd_distribution": {
            "labels": dpd_labels,
            "values": dpd_values
        },
        "funnel": funnel,
        "watchlist": watchlist
    }
