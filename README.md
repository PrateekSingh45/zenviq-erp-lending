# 🏆 ZENVIQ Individual Lending System

ZENVIQ is a comprehensive, open-source Loan Management System (LMS) and Loan Origination System (LOS) built on the robust Frappe Framework. Designed specifically for NBFCs and Fintechs, it provides an end-to-end digital lending operating system.

## 📸 Dashboard Overview
*(Add your screenshot here! Just name your image `screenshot.png`, place it in this folder, and push to GitHub).*

![ZENVIQ ERP Dashboard](screenshot.png)

## 🚀 Key Features
*   **Instant Onboarding**: RBI-compliant eKYC, PAN validation, and CIBIL integration.
*   **Automated Underwriting**: Dynamic FOIR and DTI calculation engine.
*   **Digital Signatures**: Aadhaar eSign and eNACH mandate registration.
*   **Double-Entry Accounting**: Real-time General Ledger updates upon disbursement and EMI collection.
*   **NPA & DPD Management**: Automated tracking of SMA-0, SMA-1, SMA-2, and NPA buckets with formal reporting.
*   **CEO Cockpit**: Real-time insights into AUM, Collection Efficiency, and PAR 30.

## 🛠 Tech Stack
*   **Backend**: Python, MariaDB, Redis, Frappe Framework
*   **Frontend**: Frappe UI, HTML5, CSS3, JavaScript

## 📦 Installation
Requires a standard Frappe/ERPNext bench environment.
```bash
bench get-app https://github.com/PrateekSingh45/zenviq-erp-lending.git
bench --site yoursite.local install-app zenviq_lending
```

## 📄 License
MIT License
