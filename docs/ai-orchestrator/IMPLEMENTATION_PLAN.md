# AI Orchestrator Implementation Plan

## Product Goal
Build **ZENVIQ AI**, a persistent tool-driven AI assistant in ERPNext that securely configures, analyzes, and extends the ERP based on natural-language requests. The AI uses structured ChangePlans, classifies risk, and requires human approval for sensitive changes.

## Phase 0: Setup & Assessment (Done)
- Evaluated existing Frappe/ERPNext environment.
- Documented current state in `CURRENT_ARCHITECTURE.md`.
- App target: We will implement this inside the existing `zenviq_lending` app under a new module `zenviq_ai`.

## Phase 1: Core AI Infrastructure (Current)
1. **Module Creation:** Create `zenviq_ai` module inside `zenviq_lending`.
2. **DocTypes:** 
   - `AI Change Request` (Stores intent, prompt, risk level, status, etc.)
   - `AI Change Operation` (Child table for sequential tool steps)
   - `AI Settings` (Single DocType for API keys, enabled tools, developer mode)
3. **Python Architecture:**
   - `zenviq_lending/zenviq_ai/api/`: Endpoint controllers.
   - `zenviq_lending/zenviq_ai/orchestrator/`: Context builder, intent router, planner.
   - `zenviq_lending/zenviq_ai/providers/`: Abstract AI Provider and `GeminiProvider`.
   - `zenviq_lending/zenviq_ai/tools/`: Base tool registry.
   - `zenviq_lending/zenviq_ai/policy/`: Risk and permission engine.

## Phase 2: Read-only AI
- Implement metadata inspection tools (`get_doctype_schema`, `get_system_info`).
- Implement basic ORM data query tools (read-only, permission-filtered).
- Allow user to ask system questions without mutations.

## Phase 3: Schema Tools (The MVP Goal)
- Implement schema modification tools: `create_custom_field`, `update_custom_field`.
- Implement `ChangePlan` generator schema for Gemini.
- Enforce risk classification (GREEN for non-destructive, YELLOW for edits).
- Implement human approval flow and verification API.
- Implement Rollback capability for Custom Fields.

## Phase 4-6: Advanced Agents
- **Phase 4:** Reporting & Dashboards (creating reports, charts, number cards).
- **Phase 5:** Workflow (states, transitions, approval logic).
- **Phase 6:** Automation (safe notifications, assignment rules).

## Phase 7-8: Hardening & UX Polish
- Add automated tests.
- Verify prompt injection defense (separating untrusted data).
- Build the final AI Chat UI integrated into Frappe Desk.

## MVP Success Criteria
- Execute prompt: "Add a field called Risk Category to Customer with options Low, Medium and High."
- Process: Detects `Customer` -> generates `ChangePlan` -> calculates risk (GREEN/YELLOW) -> requests human approval -> executes `create_custom_field` -> verifies -> stores audit log -> allows rollback.
