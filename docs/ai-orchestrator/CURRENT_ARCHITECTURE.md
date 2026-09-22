# Current Architecture

## Environment Overview
- **Frappe Version:** 15.118.0
- **ERPNext Version:** 15.119.3
- **HRMS Version:** 15.63.3
- **Python Version:** 3.14.2
- **Node Version:** 24.13.0
- **Database:** MariaDB 11.8 / Redis

## Installed Apps
- `frappe` (Framework)
- `erpnext` (Core ERP)
- `hrms` (HR and Payroll)
- `lending` (Frappe's Loan Management Base)
- `whitelabel` (Customization App)
- `zenviq_lending` (Custom ZENVIQ App for Individual Lending)

## ZENVIQ Specific Customizations
The `zenviq_lending` app contains customizations extending the lending base to individual lending, collections, and compliance.

### Custom DocTypes
- Borrower Profile
- Collection Action Log
- Collection Task
- Credit Assessment
- Credit Assessment Parameter
- eSign Request
- KYC Document Item
- KYC Verification
- Lending Lead
- Loan Closure Request

### UI / Desk
- Uses standard Frappe Desk and Workspaces.
- Uses standard REST APIs `/api/resource/` and `/api/method/`.
- No detached SPA (React/Vue) is currently present in the app. It's a monolith Frappe setup.

## Authentication & Authorization
- Frappe session-based Auth (Cookies / Bearer Tokens for APIs).
- Standard Role and Permissions model (System Manager, HR Manager, Sales Manager, etc.).
- `zenviq_lending` custom doctypes inherit these permission mechanisms.

## AI Orchestrator Integration Points
1. **Tool Access:** Tools will need to be written as Python methods, wrapped in standard Frappe whitelisted APIs or direct Python calls via standard module imports.
2. **Permissions:** `frappe.has_permission()` must be used inside tools to enforce user access.
3. **Audit Log:** Will require new DocTypes inside `zenviq_lending` (or a dedicated `zenviq_ai` module).
4. **Execution Layer:** We will leverage `frappe.get_doc()`, `doc.save()`, `doc.insert()`, and database transactions (`frappe.db.commit()` / `frappe.db.rollback()`).

## Reusable Existing Functionality
- `frappe.get_meta()` for schema discovery.
- `frappe.custom.doctype.custom_field.custom_field.create_custom_field` to programmatically add fields.
- Role and Permission logic built into Frappe.
- Transaction handling via `frappe.db`.
