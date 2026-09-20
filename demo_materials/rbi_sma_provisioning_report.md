# 📊 RBI SMA & NPA Classification Report (Format)

> **Document Type:** Regulatory Return (Internal & RBI/CRILC Submission Format)  
> **System:** ZENVIQ Lending System  
> **Generation Date:** September 20, 2026  
> **Reporting Period:** Current Live Snapshot

This report complies with the **Reserve Bank of India (RBI) Prudential Norms on Income Recognition, Asset Classification and Provisioning (IRACP)**. It automatically buckets loans based on Days Past Due (DPD) and calculates the required provisioning capital.

---

### 📑 Portfolio Asset Classification & Provisioning Statement

| Borrower Name | PAN Number | Loan Account | Sanction Amt (₹) | Principal O/S (₹) | Overdue (₹) | DPD | Asset Classification | Prov. Rate (%) | Prov. Amount (₹) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Rajesh Kumar Sharma** | `ABCDE1234F` | `ACC-LOAN-26-0001` | 50,000 | 41,500 | 0 | 0 | **Standard** | 0.40% | 166.00 |
| **Priya Gupta** | `BVCXZ9876Q` | `ACC-LOAN-26-0002` | 75,000 | 75,000 | 0 | 0 | **Standard** | 0.40% | 300.00 |
| **Vikram Malhotra** | `MNBVC4567L` | `ACC-LOAN-26-0003` | 1,20,000 | 1,05,000 | 35,985 | 48 | <span style="color:darkorange">**SMA-1**</span> | 0.40% | 420.00 |
| **Anita Desai** | `LKJHGF9012R` | `ACC-LOAN-26-0004` | 3,00,000 | 2,75,000 | 85,000 | 82 | <span style="color:red">**SMA-2**</span> | 0.40% | 1,100.00 |
| **Suresh Patel** | `POIUY1234T` | `ACC-LOAN-26-0005` | 1,50,000 | 1,40,000 | 1,20,000 | 115 | <span style="color:darkred">**Sub-Standard (NPA)**</span>| 15.00% | 21,000.00 |
| **Ramesh Singh** | `ZXCVB0987M` | `ACC-LOAN-25-0012` | 2,00,000 | 1,80,000 | 1,80,000 | 380 | <span style="color:black">**Doubtful (NPA)**</span> | 25.00% | 45,000.00 |
| **Sunita Devi Verma** | `QWERTY5678U` | `ACC-LOAN-25-0008` | 25,000 | 0 | 0 | 0 | **Closed / Satisfied** | 0.00% | 0.00 |

---

### 📈 Portfolio Summary

| Classification Category | DPD Criteria | Total Accounts | Total Principal O/S (₹) | Total Provision Required (₹) |
| :--- | :--- | :--- | :--- | :--- |
| **Standard / Regular** | 0 Days | 2 | 1,16,500 | 466.00 |
| **SMA-0 (Special Mention)** | 1 - 30 Days | 0 | 0 | 0.00 |
| **SMA-1 (Special Mention)** | 31 - 60 Days | 1 | 1,05,000 | 420.00 |
| **SMA-2 (Special Mention)** | 61 - 90 Days | 1 | 2,75,000 | 1,100.00 |
| **Sub-Standard (NPA)** | 91 - 365 Days | 1 | 1,40,000 | 21,000.00 |
| **Doubtful (NPA)** | > 365 Days | 1 | 1,80,000 | 45,000.00 |
| **Loss Assets** | Identified Loss | 0 | 0 | 0.00 |
| **TOTAL** | - | **6 Active** | **8,16,500** | **67,986.00** |

---

### 💡 Demo Pitch Guide for this Report

**When you show this to the client, say:**
> *"Sir/Ma'am, maintaining RBI compliance usually means your finance team spends days downloading data from the LMS, cross-referencing DPDs, and calculating NPA provisions manually in Excel to file your quarterly returns.*
> 
> *ZENVIQ comes with the RBI IRACP (Income Recognition and Asset Classification) report pre-built. The system automatically scans every loan account, maps the DPD into SMA-0, SMA-1, SMA-2, and NPA buckets, and calculates the exact capital provision you need to hold.*
> 
> *You can export this directly as a CSV and upload it to the RBI reporting portal, saving your CFO hours of manual work and completely eliminating audit risks."*
