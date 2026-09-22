# ZENVIQ Flow Design System

> Calm Productivity · Warm Neutrals · Typographic Hierarchy

## 1. Current State Analysis

- **Frappe Version**: v15 (ERPNext v15)
- **Custom App**: `zenviq_lending` with hooks-based CSS/JS injection
- **Override Strategy**: `app_include_css` and `app_include_js` in `hooks.py`
- **DocType JS**: borrower_profile.js, lending_lead.js, etc. via `doctype_js` hooks
- **Custom Pages**: `zenviq_home` (Lending), `owner-cockpit` (Insights)

### UX Problems Identified
1. **Top-heavy layout**: Stacked navbar + page header + workspace title wastes vertical space
2. **Cold palette**: Generic SaaS blue-gray feels clinical, not warm
3. **Over-decoration**: Excessive cards, shadows, borders, gradients compete with content
4. **Database orientation**: Screens reflect DocType schemas rather than operational workflows
5. **Cockpit routing bug**: JSON `name` field used hyphen (`owner-cockpit`) but JS registered with underscore

## 2. Design Philosophy

**Calm Productivity** — the interface should disappear behind the work.

Users should notice: Borrowers, Loans, Approvals, Collections, Risk, ZENVIQ Intelligence. 
Users should NOT notice: navigation chrome, cards, buttons, borders, ERPNext modules.

## 3. Design Tokens

| Token | Value | Usage |
|---|---|---|
| `--z-shell` | `#F5F4F0` | Application background |
| `--z-surface` | `#FFFFFF` | Primary workspace |
| `--z-surface-soft` | `#FAF9F6` | Secondary surfaces |
| `--z-surface-metric` | `#F8F7F4` | Metric cards |
| `--z-accent` | `#6C5CE7` | ZENVIQ purple (AI, identity) |
| `--z-positive` | `#176B62` | Approved, positive financial status |
| `--z-text` | `#1E1E1C` | Primary text |
| `--z-text-secondary` | `#64615C` | Secondary text |
| `--z-text-muted` | `#8A8781` | Metadata, labels |
| `--z-border` | `#E5E2DB` | Borders |
| `--z-radius-workspace` | `24px` | Primary workspace container |
| `--z-radius-card` | `12px` | Metric cards, panels |
| `--z-radius-control` | `8px` | Inputs, buttons, nav items |

## 4. Typography

- **Primary**: Figtree (Google Fonts)
- **Editorial**: Instrument Serif (AI insight headings only)
- **Scale**: Title 28px/600, Metric 32px/500, Section 17px/600, Body 14px/400, Nav 14px/500, Meta 12px/400

## 5. Sidebar Architecture

- Fixed left, 250px, warm shell background (`#F5F4F0`)
- Sections: Overview, Lending, Intelligence, System
- Active state: `#ECE9E2` background, `#20201E` text
- User profile anchored at bottom with border-top separator

## 6. Workspace Architecture

- Single large white container with `24px` border radius
- Inner padding: `44px 48px`
- No nested cards for form sections (transparent background)
- Max content width: ~1100px for dashboards

## 7. ERPNext Override Strategy

- **CSS**: Global `zenviq_theme.css` via `app_include_css`
- **JS**: Global `zenviq_shell.js` via `app_include_js`
- **DocType JS**: Per-doctype via `doctype_js` hook
- **Custom Pages**: `zenviq_home`, `owner-cockpit`
- **NO core modifications** to Frappe or ERPNext

## 8. Implementation Phases

| Phase | Scope | Status |
|---|---|---|
| 0 | Audit | Done |
| 1 | Design tokens, shell, typography | Done |
| 2 | Sidebar, navigation, user area | Done |
| 3 | Lending home | Done |
| 4 | Owner Cockpit / Insights | Done |
| 5 | Lists, forms, buttons, tabs | Done |
| 6 | Loan Application detail | Planned |
| 7 | Borrower Profile | Planned |
| 8-13 | Collections, My Work, AI, Accounting, Polish | Planned |
