# ZENVIQ Current UI Architecture

## Overview
ZENVIQ ERP is currently running as a custom Frappe application (`zenviq_lending`) on top of Frappe Framework v15 (15.118.0) and ERPNext v15 (15.119.3). 

## Existing Implementations

### 1. Framework & Dependencies
* **Core:** Frappe 15 / ERPNext 15
* **CSS/JS Stack:** Frappe standard stack (Vue.js for some components, jQuery for legacy parts, Frappe UI, Bootstrap grids, CSS variables).
* **Installed Apps:** `erpnext`, `frappe`, `hrms`, `lending`, `whitelabel`, `zenviq_lending`.

### 2. Workspace & Shell
* **Global Navbar:** Standard Frappe v15 navbar (Search, Help, Notifications, User).
* **Sidebar:** Standard Frappe Desk sidebar with default modules listed vertically. No collapsed-icon-only mode out of the box, standard active state styling.
* **Workspace (`ZENVIQ Lending`):** 
  - Standard JSON-based Frappe Workspace.
  - Header: `ZENVIQ Individual Lending Management` (h3), sub-text.
  - Number Cards: 4 basic KPI cards (`Total Active Loans`, etc.).
  - Shortcuts: 13 vertical shortcuts stacked underneath (CEO Cockpit, Leads, Borrowers, KYC, etc.). Very flat structure, relies on basic anchor tags and icons.

### 3. ZENVIQ AI Orchestrator UI
* The AI Orchestrator page (`zenviq_ai_chat.js`) has recently been refactored into a custom DOM architecture that replaces the standard Frappe layout with a dual-pane workspace (Sidebar + Main Chat Area), using absolute/flex positioning and modern design tokens (`#F8FAFC`, `#0F172A`, linear gradients).
* *Note:* This AI UI currently looks disjointed from the rest of the application since the rest of the application is standard Frappe UI.

### 4. Customization Vectors (Safe Overrides)
To modernize the ERP without breaking core files, we can utilize:
1. **`hooks.py` (`app_include_css`, `app_include_js`):** Inject global design tokens, CSS variable overrides, and JS scripts to manipulate the Navbar and Sidebar DOM across the entire application shell.
2. **Workspace JSON Definitions:** Modify the layout of the workspaces via backend queries or by exporting customized Workspace fixtures.
3. **Custom Page Development:** For complex dashboards (like the Owner Cockpit), use `frappe.ui.make_app_page` inside custom pages.
4. **Client Scripts / Doctype JS:** Customize list and form views on a per-doctype basis.

## Critical Constraints
- **Upgradability:** Direct modification of `frappe` or `erpnext` codebase is prohibited.
- **Functionality:** Existing routing, permissions, and DocType logic must remain 100% intact.
- **Responsiveness:** Changes to the DOM structure must account for Frappe's mobile breakpoints.
