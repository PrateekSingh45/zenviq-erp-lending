# ZENVIQ Design System & Implementation Plan

## Vision
Transform the default ERPNext interface into a premium, AI-native enterprise operating system. It must communicate Intelligence, Control, Clarity, Trust, Speed, and Automation, moving away from a traditional "forms and tables" ERP to an "insight and action" CRM-like experience.

## 1. Design Tokens & Semantic Colors
* **Primary Brand:** ZENVIQ Indigo (`#635BFF`)
* **AI Accent:** Violet (`#8B5CF6`) / Subtle gradient (`linear-gradient(135deg, #635BFF 0%, #7C5CFC 45%, #9B6CFF 100%)`)
* **Backgrounds:** Global App Background (`#F7F8FA`), Surfaces (`#FFFFFF`), Secondary (`#FAFAFB`), Sidebar (`#F9FAFB`).
* **Text:** Primary (`#18181B`), Secondary (`#52525B`), Muted (`#71717A`).
* **Borders & Radii:** Subtle borders (`#ECEDEF`), UI radii (6px controls, 8px inputs, 12px cards).
* **Typography:** `Inter` / System UI stack. 

## 2. Phase 1: Global Shell & Tokens (Immediate Focus)
* **CSS Variable Injection:** Use `app_include_css` to inject CSS overriding Frappe's native variables (`--bg-color`, `--text-color`, `--border-color`, etc.) with our new token system.
* **Top Navbar:**
  - Redesign search to act as a Command Palette ("Search records, pages, or ask ZENVIQ...").
  - Inject the global "✨ Ask ZENVIQ" button.
* **Sidebar:**
  - Inject CSS to alter padding, active states (`#F0EFFF` bg with `#635BFF` text/icon).
  - Modernize the scrollbar and spacing.

## 3. Phase 2: ZENVIQ Lending Workspace / Home (Immediate Focus)
* Override the standard Frappe Workspace view for "ZENVIQ Lending".
* Build a custom HTML/JS layout or heavily inject CSS into the existing workspace DOM to render:
  - Header with business context.
  - KPI Overview Cards (AUM, Active Loans, PAR30).
  - "Needs Attention" and "Lending Pipeline" functional sections.
  - "✦ ZENVIQ Insight" agentic card.

## 4. Future Phases
* **Phase 3 & 4:** Modernize List Views (checkboxes, inline actions, compact row heights) and Form Views (progressive disclosure, sticky action bars).
* **Phase 5 & 6:** Entity CRM Pages (Borrower Overview combining multiple lists into tabs) and Executive Cockpit (Visual Dashboards).
* **Phase 8:** Deep AI Contextual Integration (Side-panel slide-outs).

## Execution Strategy
- All design tokens will be centralized in `zenviq_theme.css`.
- Shell DOM manipulation (e.g., adding the "Ask ZENVIQ" button to the Frappe navbar) will be handled via a global script `zenviq_shell.js` included via `hooks.py`.
- We will visually verify layout at 1366x768, 1440x900, and 1920x1080 before proceeding to subsequent phases.
