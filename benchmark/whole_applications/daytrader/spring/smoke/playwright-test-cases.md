# Daytrader - Playwright Test Cases

## Overview
This document outlines comprehensive Playwright test cases for the Eclipse Daytrader application, a Jakarta EE demonstration application that showcases a day trading platform with various features.

**Base URL:** http://localhost:9080/daytrader/

## Test Case Categories
**1. Global / Smoke / Navigation**

- **Home / welcome page**: Load `/daytrader/` and `/daytrader/welcome.jsp`; verify title, main heading, introductory text, and key links (Login, Register, Quotes, Portfolio, Help/Docs).
- **Top navigation**: From multiple pages, click nav links (Home, Login, Register, Market Summary, Portfolio, Trade, Config, Docs) and assert URL, heading, and content change as expected.
- **Header / footer consistency**: Verify logo, app name, and footer content are present and consistent on all main pages.
- **Protected pages redirect**: Try visiting `/portfolio.jsp`, `/tradehome.jsp`, `/order.jsp`, `/runStats.jsp` while not logged in; confirm redirect to login or a clear access error.
- **404 / invalid URL**: Visit a nonexistent path under `/daytrader/` and assert friendly error page (no raw stack trace).
- **Static resources**: On one or two pages, assert CSS (`style.css`, `style-jsf.css`) and key JS files load successfully (no 404), console is free of severe errors.

---

**2. Authentication (Login / Logout)**

- **Render login page**: Check username/password fields, submit button, links back to home/register, and any “remember me” or info text.
- **Empty credentials**: Submit with both fields empty; assert validation error and no navigation.
- **Partial credentials**: Submit with username only or password only; verify appropriate error.
- **Invalid credentials**: Use wrong password for an existing user; verify clear error message and still unauthenticated.
- **Successful login**: Login as a known user; expect redirect to `tradehome` or `portfolio`, display of username, and updated navigation (e.g., Logout becomes visible).
- **Session continuity**: After login, navigate across multiple pages (Portfolio, Quotes, Order, Run Stats) and verify user remains logged in.
- **Logout**: Click Logout; assert redirect to public home, username no longer shown, and protected pages now redirect or deny access.

---

**3. Registration / New Account**

- **Render registration page**: Check all fields (username, password, confirm password, full name, email, address, credit card/initial balance or similar), and explanatory help text.
- **Required field validation**: Try submitting with:
  - All fields empty.
  - Missing only username.
  - Missing only password/confirm password.
  - Missing email.
- **Password rules**: If password length/complexity rules exist, test too-short/invalid passwords and assert errors.
- **Password confirmation**: Enter mismatched passwords; verify clear message and no account creation.
- **Email validation**: Enter invalid email formats; assert validation.
- **Negative/zero balance**: Provide invalid values for initial balance or credit-related fields and verify error.
- **Duplicate username**: Attempt to register a username that already exists; assert uniqueness error.
- **Successful registration**: Register a new, unique user; assert success message and:
  - Either automatic login with redirect to tradehome/portfolio, or
  - Explicit prompt to log in with new credentials.
- **Post-registration login**: Log out (if auto-logged-in) and confirm new credentials can log in successfully.

---

**4. Account / Profile Management**

- **Account/summary page**: After login, open account info page (`account.jsp`/`account.xhtml`); ensure correct user data (name, address, email, balance, etc.) is displayed.
- **Edit account details**: Change address or other editable fields, save, and verify:
  - Success message.
  - Updated values appear immediately.
  - Values persist after page reload and new session (log out, log in again).
- **Read-only fields**: Confirm fields that should not be editable (e.g., username, account ID) cannot be changed.

---

**5. Portfolio**

- **Empty portfolio for new user**: For a newly created user with no trades, open `portfolio.jsp`; verify:
  - Empty-state messaging.
  - No holdings rows.
  - Links/buttons to start trading (Buy/Quotes/Market Summary).
- **Populated portfolio**: After some buy trades, confirm:
  - Each holding row shows symbol, company name (if present), quantity, price, total value, and gain/loss.
  - Overall portfolio totals and cash balance display correctly.
- **Row actions**: On a holding row, use available actions (e.g., Sell, View Quote) and confirm navigation to correct pages with symbol pre-populated.
- **Refresh behavior**: Reload the portfolio page:
  - Data and totals remain consistent.
  - No duplicate rows or stale values.
- **Sorting / ordering (if present)**: If the portfolio supports sorting by symbol or value, verify clicking headers changes order as expected.

---

**6. Quotes & Market Summary**

- **Market summary page**: Visit `marketSummary.jsp`/`marketSummary.xhtml`:
  - Verify list of top symbols with last price, change, and volume.
  - Confirm summary totals/index (if present).
- **Quote lookup – valid symbol**:
  - Use the quote lookup form on `quote.jsp` or trade home.
  - Enter a valid symbol (e.g., from summary list).
  - Assert resulting detail page shows correct symbol, company name, last price, day high/low, volume.
- **Quote lookup – invalid symbol**: Enter a clearly invalid symbol; verify:
  - Clear error/“symbol not found” message.
  - No crash or unhandled exception.
- **Repeated lookups**: Perform multiple consecutive lookups for different symbols in one session; check:
  - Each result updates accordingly.
  - Back/forward navigation behaves sensibly.
- **Links from quote to actions**: From a quote detail page, click Buy/Sell links and verify routing to order page with symbol pre-filled.

---

**7. Trading – Buy / Sell Orders**

- **Buy order from quote**:
  - Start from a quote page; click Buy.
  - Ensure symbol is pre-filled, quantity field available, price or estimated cost shown, and Buy/Cancel buttons present.
- **Buy validation – quantity**:
  - Quantity zero or empty.
  - Negative quantity.
  - Very large quantity (beyond configured limits, if any).
  - Assert inline errors and prevention of submission.
- **Buy validation – funds**:
  - If enforced, attempt a purchase that exceeds available cash; assert “insufficient funds” behavior.
- **Successful buy**:
  - Submit a valid buy order.
  - Verify confirmation screen (symbol, quantity, price, total).
  - Check portfolio:
    - New holding appears or quantity for existing symbol increases.
    - Cash balance decreases appropriately.
- **Sell order from portfolio**:
  - From `portfolio.jsp`, initiate a Sell for a holding.
  - Verify symbol and current quantity displayed.
- **Sell validation – quantity**:
  - Try to sell more than owned; assert error.
  - Zero/negative quantity; assert error.
- **Successful sell**:
  - Submit valid sell order.
  - Confirm:
    - Quantity is reduced or holding removed when quantity hits zero.
    - Cash balance increases.
  - Order history/run stats updated (see below).
- **Cancel actions**: On order forms, use Cancel/back buttons and verify:
  - Navigation returns to origin page (portfolio or quote).
  - No order is created.

---

**8. Order History / Run Stats**

- **Run stats page**: Open `runStats.jsp`:
  - Verify overall trading metrics, number of users, orders, completed trades, etc. display correctly.
- **User-level order history (if present)**:
  - Ensure list of recent orders for the current user appears with symbol, side (buy/sell), quantity, price, timestamp, and status.
- **New order visibility**:
  - After placing buys/sells, verify those orders appear in the history with correct details and status.
- **Filtering / paging (if available)**:
  - Test next/previous page or filter parameters and confirm list updates correctly.

---

**9. Trade Home / Dashboard**

- **Post-login trade home**:
  - Verify presence of: account summary (cash, portfolio value), quick quote input, quick links to Portfolio/Market Summary/Order pages, and maybe a recent-activity widget.
- **Quick quote**:
  - Enter symbol in the quick quote box; assert it shows result or navigates to quote detail.
- **Quick trade shortcuts**:
  - If there are “Buy” buttons directly from summary widgets, test they go to order page with expected context.
- **Consistency with other pages**:
  - Verify balances and holdings summary on trade home match detailed portfolio view.

---

**10. Configuration / Admin**

- **Access control**:
  - Attempt to reach `config.jsp` as:
    - Unauthenticated user → expect redirect/denial.
    - Regular user → if restricted to admin, expect denial.
    - Admin user (if such role exists) → expect full access.
- **Config options render**:
  - Validate presence of runtime options (e.g., order processing mode, database mode, WS vs JMS, test data reset, etc.).
- **Modify configuration**:
  - Change a safe option (e.g., toggle between some modes or enable/disable a non-destructive feature), click Apply, and verify:
    - Success message.
    - Value persists after reload.
- **Dangerous operations**:
  - If a “reset database” or “repopulate” button exists, verify:
    - Warnings/confirmation prompts are shown.
    - Operation either succeeds (with test data) or is not accidentally triggered.
- **Non-admin behavior**:
  - Confirm non-admin cannot perform privileged actions (buttons disabled/hidden or operations denied).

---

**11. Special / Diagnostic Pages (Ping & WebSocket)**

- **Ping pages (`PingHtml`, `PingJsp`, `PingJsf`, `PingServlet2Jsp`)**:
  - Visit each ping page; verify:
    - Page loads without error.
    - Shows expected “ping success” or diagnostic text.
- **WebSocket test pages** (`PingWebSocketTextSync`, `PingWebSocketTextAsync`, `PingWebSocketJson`, `PingWebSocketBinary`):
  - Open each WS page:
    - Confirm connection status indicator shows connected.
    - Send a test message via UI.
    - Assert expected echo/response appears in UI within a reasonable time.
    - Test reconnect or error display if connection is dropped (if UI supports it).

---

**12. Documentation / Help Pages**

- **Docs / FAQ (`docs/tradeFAQ.html` and similar)**:
  - Open docs pages from UI links; assert:
    - Correct headings and navigation within docs.
    - Back to application links work.
- **Primitive web page (`web_prmtv.html`/`.xhtml`)**:
  - Validate static content loads and any sample links navigate correctly.

---

**13. Error Handling & Edge Cases**

- **Malformed parameters**:
  - Manually alter query parameters (e.g., invalid order IDs, non-numeric quantities in URL) via `page.goto`.
  - Assert graceful error messages, not raw stack traces.
- **Concurrent changes (basic)**:
  - In two browser contexts (or two tests), place trades for same symbol; verify that UI remains consistent (e.g., no visible corruption).
- **Session timeout**:
  - If feasible, simulate session expiry (e.g., wait expected timeout duration or call backend to invalidate), then:
    - Attempt navigation or order placement.
    - Assert redirect to login with a message.

---

**14. UX & Accessibility (High Level)**

- **Keyboard navigation**:
  - For login, register, quote lookup, and order forms:
    - Ensure Tab/Shift+Tab navigate fields in logical order.
    - Enter/Space triggers buttons appropriately.
- **Focus management**:
  - On validation errors, check that focus moves (or is clearly guided) to problem fields.
- **Labels and semantics**:
  - Verify each input has a visible label and that form controls are screen-reader friendly (Playwright’s `getByRole`/`getByLabel` selectors should work).
- **Contrast / visibility**:
  - Check that primary text and buttons are readable on default theme.
- **Announcements (if any modals/toasts)**:
  - For any confirmation dialogs or toasts, assert they appear, are dismissible, and do not trap focus.

---

**15. Performance / Basic Health Checks**

- **Initial page load time**:
  - Measure approximate time for home, login, and portfolio pages; assert within a reasonable local threshold.
- **JS errors on navigation**:
  - For a representative flow (login → tradehome → portfolio → quote → order → runStats), assert no uncaught exceptions in browser console.
- **Resource caching (light check)**:
  - Ensure repeated navigation does not cause obvious resource-load failures or layout thrash.
