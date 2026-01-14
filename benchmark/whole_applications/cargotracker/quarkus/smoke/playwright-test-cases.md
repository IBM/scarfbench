# Cargo Tracker - Playwright Test Cases

## Overview
This document outlines comprehensive Playwright test cases for the Eclipse Cargo Tracker application, a Jakarta EE demonstration application that showcases Domain-Driven Design principles.

**Base URL:** http://localhost:8080/cargo-tracker/

---

## 1. Home Page Tests

### Test 1.1: Verify Home Page Loads
**Description:** Validate that the home page loads successfully with all expected elements.

**Steps:**
1. Navigate to `http://localhost:8080/cargo-tracker/`
2. Verify page title is "Eclipse Cargo Tracker"
3. Verify main heading contains "Eclipse Cargo Tracker"
4. Verify subtitle contains "Applied Domain-Driven Design Blueprints for Jakarta EE"
5. Verify Cargo Tracker logo is visible
6. Verify three main buttons are present:
   - "Public Tracking Interface"
   - "Administration"
   - "Event Logging Interface"

### Test 1.2: Navigate to Public Tracking Interface
**Description:** Test navigation from home page to public tracking interface.

**Steps:**
1. Navigate to home page
2. Click on "Public Tracking Interface" button
3. Verify URL changes to `/public/track.xhtml`
4. Verify page loads successfully

### Test 1.3: Navigate to Administration Interface
**Description:** Test navigation from home page to administration dashboard.

**Steps:**
1. Navigate to home page
2. Click on "Administration" button
3. Verify URL changes to `/admin/dashboard.xhtml`
4. Verify page loads successfully

### Test 1.4: Open Event Logging Interface Popup
**Description:** Test that event logging interface opens in a new popup window.

**Steps:**
1. Navigate to home page
2. Click on "Event Logging Interface" button
3. Verify a new window/popup opens with URL `/event-logger/index.xhtml`
4. Verify popup window dimensions (width=320, height=440)

---

## 2. Public Tracking Interface Tests

### Test 2.1: Verify Public Tracking Page Structure
**Description:** Validate the structure and elements of the public tracking page.

**Steps:**
1. Navigate to `http://localhost:8080/cargo-tracker/public/track.xhtml`
2. Verify page title is "Track Cargo"
3. Verify side menu contains:
   - Cargo Tracker logo
   - "Tracking" menu item
   - "About" menu item
4. Verify tracking form is present with:
   - Input field with placeholder "XYZ789"
   - "Track!" submit button

### Test 2.2: Track Valid Cargo - ABC123
**Description:** Test tracking a valid cargo with ID ABC123.

**Steps:**
1. Navigate to public tracking page
2. Enter "ABC123" in the tracking ID input field
3. Click "Track!" button
4. Verify cargo status information is displayed
5. Verify cargo details show:
   - Origin: Hong Kong (CNHKG)
   - Destination: Helsinki (FIHEL)
   - Status information

### Test 2.3: Track Valid Cargo - JKL567
**Description:** Test tracking another valid cargo with ID JKL567.

**Steps:**
1. Navigate to public tracking page
2. Enter "JKL567" in the tracking ID input field
3. Click "Track!" button
4. Verify cargo status information is displayed
5. Verify cargo details show:
   - Origin: Hangzhou (CNHGH)
   - Destination: Stockholm (SESTO)

### Test 2.4: Track Valid Cargo - DEF789
**Description:** Test tracking an unrouted cargo with ID DEF789.

**Steps:**
1. Navigate to public tracking page
2. Enter "DEF789" in the tracking ID input field
3. Click "Track!" button
4. Verify cargo status information is displayed
5. Verify cargo shows as not routed

### Test 2.5: Track Valid Cargo - MNO456
**Description:** Test tracking a claimed cargo with ID MNO456.

**Steps:**
1. Navigate to public tracking page
2. Enter "MNO456" in the tracking ID input field
3. Click "Track!" button
4. Verify cargo status information is displayed
5. Verify cargo shows as claimed

### Test 2.6: Track Invalid Cargo ID
**Description:** Test error handling for invalid tracking ID.

**Steps:**
1. Navigate to public tracking page
2. Enter "INVALID999" in the tracking ID input field
3. Click "Track!" button
4. Verify appropriate error message or "not found" indication is displayed

### Test 2.7: Submit Empty Tracking ID
**Description:** Test form validation for empty tracking ID.

**Steps:**
1. Navigate to public tracking page
2. Leave tracking ID input field empty
3. Click "Track!" button
4. Verify form validation message appears (field is required)

### Test 2.8: Navigate to About Page from Public Tracking
**Description:** Test navigation to About page from public tracking interface.

**Steps:**
1. Navigate to public tracking page
2. Click on "About" menu item in side panel
3. Verify URL changes to `/public/about.xhtml`
4. Verify About page content loads

---

## 3. Administration Dashboard Tests

### Test 3.1: Verify Dashboard Structure
**Description:** Validate the structure and elements of the admin dashboard.

**Steps:**
1. Navigate to `http://localhost:8080/cargo-tracker/admin/dashboard.xhtml`
2. Verify page title is "Cargo Dashboard"
3. Verify side menu contains:
   - Cargo Tracker logo
   - "Dashboard" menu item
   - "Book" menu item
   - "Track" menu item
   - "Live" menu item
   - "About" menu item
4. Verify three cargo tables are present:
   - "Routed Cargo"
   - "Not Routed Cargo"
   - "Claimed Cargo"

### Test 3.2: Verify Routed Cargo Table
**Description:** Validate the routed cargo table displays correct information.

**Steps:**
1. Navigate to admin dashboard
2. Locate "Routed Cargo" section
3. Verify table has columns:
   - Tracking ID
   - Origin
   - Destination
   - Last Known Location
   - Status
   - Deadline
4. Verify at least two cargoes are listed:
   - ABC123 (Hong Kong → Helsinki)
   - JKL567 (Hangzhou → Stockholm)

### Test 3.3: Verify Not Routed Cargo Table
**Description:** Validate the not routed cargo table displays correct information.

**Steps:**
1. Navigate to admin dashboard
2. Locate "Not Routed Cargo" section
3. Verify table has columns:
   - Tracking ID
   - Origin
   - Destination
   - Deadline
4. Verify DEF789 is listed (Hong Kong → Melbourne)
5. Verify edit icons are present for destination and deadline

### Test 3.4: Verify Claimed Cargo Table
**Description:** Validate the claimed cargo table displays correct information.

**Steps:**
1. Navigate to admin dashboard
2. Locate "Claimed Cargo" section
3. Verify table has columns:
   - Tracking ID
   - Origin
   - Destination
   - Deadline
4. Verify MNO456 is listed (New York → Dallas)

### Test 3.5: Click Routed Cargo Details - ABC123
**Description:** Test viewing details of routed cargo ABC123.

**Steps:**
1. Navigate to admin dashboard
2. In "Routed Cargo" table, click on "ABC123" tracking ID link
3. Verify URL changes to `/admin/show.xhtml?trackingId=ABC123`
4. Verify cargo details page loads with itinerary information

### Test 3.6: Click Routed Cargo Details - JKL567
**Description:** Test viewing details of routed cargo JKL567.

**Steps:**
1. Navigate to admin dashboard
2. In "Routed Cargo" table, click on "JKL567" tracking ID link
3. Verify URL changes to `/admin/show.xhtml?trackingId=JKL567`
4. Verify cargo details page loads

### Test 3.7: Click Not Routed Cargo for Routing - DEF789
**Description:** Test navigating to route a cargo that hasn't been routed yet.

**Steps:**
1. Navigate to admin dashboard
2. In "Not Routed Cargo" table, click on "DEF789" tracking ID link
3. Verify URL changes to `/admin/route.xhtml?trackingId=DEF789`
4. Verify routing page loads

### Test 3.8: View Claimed Cargo Details - MNO456
**Description:** Test viewing history of claimed cargo MNO456.

**Steps:**
1. Navigate to admin dashboard
2. In "Claimed Cargo" table, click on "MNO456" tracking ID link
3. Verify URL changes to `/admin/show.xhtml?trackingId=MNO456`
4. Verify cargo history page loads

### Test 3.9: Tooltip Verification - Routed Cargo
**Description:** Test that tooltips appear on hover for routed cargo.

**Steps:**
1. Navigate to admin dashboard
2. Hover over the info icon next to ABC123 tracking ID
3. Verify tooltip appears with text "Click to see itinerary's details."

### Test 3.10: Tooltip Verification - Not Routed Cargo
**Description:** Test that tooltips appear for not routed cargo.

**Steps:**
1. Navigate to admin dashboard
2. Hover over the globe icon next to DEF789 tracking ID
3. Verify tooltip appears with text "This cargo is not routed. Click on its tracking ID to route it!"

### Test 3.11: Change Cargo Destination
**Description:** Test changing the destination of a not routed cargo.

**Steps:**
1. Navigate to admin dashboard
2. In "Not Routed Cargo" table, click the edit icon next to destination for DEF789
3. Verify destination change dialog/form appears
4. Verify can select a new destination

### Test 3.12: Change Arrival Deadline
**Description:** Test changing the arrival deadline of a not routed cargo.

**Steps:**
1. Navigate to admin dashboard
2. In "Not Routed Cargo" table, click the edit icon next to deadline for DEF789
3. Verify deadline change dialog/form appears
4. Verify can select a new deadline date

---

## 4. Book New Cargo Tests

### Test 4.1: Start Booking Flow from Dashboard
**Description:** Test initiating cargo booking from the dashboard menu.

**Steps:**
1. Navigate to admin dashboard
2. Click on "Book" menu item
3. Verify booking interface/flow is initiated
4. Verify booking form is displayed

### Test 4.2: Book New Cargo - Complete Flow
**Description:** Test complete cargo booking workflow (if booking flow is accessible).

**Steps:**
1. Navigate to admin dashboard
2. Click on "Book" menu item
3. Select origin location
4. Select destination location
5. Select arrival deadline
6. Submit booking
7. Verify new cargo is created
8. Verify redirect to appropriate page (dashboard or cargo details)

### Test 4.3: Booking Form Validation - Missing Origin
**Description:** Test validation when origin is not provided.

**Steps:**
1. Start booking flow
2. Leave origin field empty
3. Fill in destination and deadline
4. Attempt to submit
5. Verify validation error for origin field

### Test 4.4: Booking Form Validation - Missing Destination
**Description:** Test validation when destination is not provided.

**Steps:**
1. Start booking flow
2. Fill in origin
3. Leave destination field empty
4. Fill in deadline
5. Attempt to submit
6. Verify validation error for destination field

### Test 4.5: Booking Form Validation - Missing Deadline
**Description:** Test validation when deadline is not provided.

**Steps:**
1. Start booking flow
2. Fill in origin and destination
3. Leave deadline field empty
4. Attempt to submit
5. Verify validation error for deadline field

### Test 4.6: Booking Form - Same Origin and Destination
**Description:** Test validation when origin and destination are the same.

**Steps:**
1. Start booking flow
2. Select same location for origin and destination
3. Fill in deadline
4. Attempt to submit
5. Verify appropriate validation error

---

## 5. Cargo Routing Tests

### Test 5.1: Access Routing Page for Unrouted Cargo
**Description:** Navigate to routing page for cargo DEF789.

**Steps:**
1. Navigate to `http://localhost:8080/cargo-tracker/admin/route.xhtml?trackingId=DEF789`
2. Verify page loads successfully
3. Verify cargo information is displayed:
   - Origin: Hong Kong
   - Destination: Melbourne
   - Deadline date

### Test 5.2: View Available Itineraries
**Description:** Test viewing available routing itineraries for a cargo.

**Steps:**
1. Navigate to routing page for DEF789
2. Verify list of available itineraries is displayed
3. Verify each itinerary shows:
   - Route legs (voyage numbers)
   - Departure and arrival locations
   - Estimated times

### Test 5.3: Select an Itinerary
**Description:** Test selecting an itinerary to route the cargo.

**Steps:**
1. Navigate to routing page for DEF789
2. View available itineraries
3. Click on "Select" button for a specific itinerary
4. Verify confirmation or redirect to itinerary details page
5. Navigate back to dashboard
6. Verify DEF789 has moved from "Not Routed" to "Routed" table

### Test 5.4: Routing Page - No Available Routes
**Description:** Test routing page behavior when no routes are available (edge case).

**Steps:**
1. Create a cargo with origin/destination that have no routes (if possible)
2. Navigate to routing page for that cargo
3. Verify appropriate message indicating no routes available

---

## 6. Cargo Details/Show Page Tests

### Test 6.1: View Cargo Details Page - ABC123
**Description:** Test viewing detailed information for routed cargo ABC123.

**Steps:**
1. Navigate to `http://localhost:8080/cargo-tracker/admin/show.xhtml?trackingId=ABC123`
2. Verify page loads successfully
3. Verify cargo information is displayed:
   - Tracking ID: ABC123
   - Origin: Hong Kong (CNHKG)
   - Destination: Helsinki (FIHEL)
   - Routing status
   - Current location
   - Deadline

### Test 6.2: View Cargo Itinerary Details
**Description:** Test that itinerary details are shown on cargo details page.

**Steps:**
1. Navigate to show page for ABC123
2. Verify itinerary section displays route legs
3. Verify each leg shows:
   - Voyage number
   - From location
   - To location
   - Load/unload times (if available)

### Test 6.3: View Cargo Handling History
**Description:** Test viewing handling events history for a cargo.

**Steps:**
1. Navigate to show page for ABC123
2. Locate handling history section
3. Verify handling events are listed chronologically
4. Verify each event shows:
   - Event type (RECEIVE, LOAD, UNLOAD, etc.)
   - Location
   - Voyage (if applicable)
   - Timestamp

### Test 6.4: View Cargo Status Information
**Description:** Test that cargo status is clearly displayed.

**Steps:**
1. Navigate to show page for JKL567
2. Verify current status is shown (e.g., "ONBOARD_CARRIER")
3. Verify last known location is displayed
4. Verify estimated arrival information (if available)

### Test 6.5: Navigate to Map View from Details
**Description:** Test navigation to map view (if link exists).

**Steps:**
1. Navigate to show page for ABC123
2. Look for map view link/button
3. If present, click on it
4. Verify map interface loads showing cargo location

---

## 7. Admin Tracking Interface Tests

### Test 7.1: Access Admin Track Page
**Description:** Navigate to admin tracking interface.

**Steps:**
1. Navigate to admin dashboard
2. Click on "Track" menu item
3. Verify URL changes to `/admin/tracking/track.xhtml`
4. Verify tracking interface loads

### Test 7.2: Track Cargo from Admin Interface
**Description:** Test cargo tracking functionality from admin interface.

**Steps:**
1. Navigate to admin track page
2. Verify tracking input field is present
3. Enter tracking ID (e.g., "ABC123")
4. Submit tracking request
5. Verify cargo information is displayed

---

## 8. Live Map Interface Tests

### Test 8.1: Access Live Map Page
**Description:** Navigate to live tracking map interface.

**Steps:**
1. Navigate to admin dashboard
2. Click on "Live" menu item
3. Verify URL changes to `/admin/tracking/map.xhtml`
4. Verify map interface loads

### Test 8.2: Verify Map Loads
**Description:** Test that the map component loads successfully.

**Steps:**
1. Navigate to live map page
2. Verify map container is present
3. Verify Leaflet.js map library loads (check for map tiles)
4. Verify map controls are functional (zoom, pan)

### Test 8.3: View Cargo Markers on Map
**Description:** Test that cargo locations are shown as markers on the map.

**Steps:**
1. Navigate to live map page
2. Wait for map to fully load
3. Verify markers/pins are displayed for active cargoes
4. Verify markers are positioned at appropriate locations

### Test 8.4: Click Cargo Marker for Details
**Description:** Test interaction with cargo markers on map.

**Steps:**
1. Navigate to live map page
2. Click on a cargo marker/pin
3. Verify popup/tooltip appears with cargo information:
   - Tracking ID
   - Current location
   - Status
4. Verify link to cargo details (if available)

---

## 9. About Pages Tests

### Test 9.1: Access Public About Page
**Description:** Navigate to public about page.

**Steps:**
1. Navigate to public tracking interface
2. Click on "About" menu item
3. Verify URL changes to `/public/about.xhtml`
4. Verify about page content loads

### Test 9.2: Access Admin About Page
**Description:** Navigate to admin about page.

**Steps:**
1. Navigate to admin dashboard
2. Click on "About" menu item
3. Verify URL changes to `/admin/about.xhtml`
4. Verify about page content loads

### Test 9.3: Verify About Page Content
**Description:** Validate content on about page.

**Steps:**
1. Navigate to about page
2. Verify information about Cargo Tracker application is present
3. Verify information about Domain-Driven Design is present
4. Verify technology stack information (Jakarta EE, etc.)
5. Verify links to GitHub repository (if present)

---

## 10. Event Logger Interface Tests

### Test 10.1: Access Event Logger Interface
**Description:** Navigate to event logger interface.

**Steps:**
1. Navigate to home page
2. Click on "Event Logging Interface" button
3. Verify popup window opens with URL `/event-logger/index.xhtml`
4. Verify event logger interface loads

### Test 10.2: View Event Logging Form
**Description:** Validate the structure of event logging form.

**Steps:**
1. Open event logger interface
2. Verify form contains fields for:
   - Tracking ID
   - Event type selection (dropdown or radio buttons)
   - Location
   - Voyage (if applicable)
   - Completion time
3. Verify submit button is present

### Test 10.3: Log Handling Event - RECEIVE
**Description:** Test logging a RECEIVE event for a cargo.

**Steps:**
1. Open event logger interface
2. Enter tracking ID (e.g., "DEF789")
3. Select event type: RECEIVE
4. Select location
5. Enter/select completion time
6. Submit event
7. Verify success message or confirmation

### Test 10.4: Log Handling Event - LOAD
**Description:** Test logging a LOAD event for a cargo.

**Steps:**
1. Open event logger interface
2. Enter tracking ID (e.g., "ABC123")
3. Select event type: LOAD
4. Select location
5. Enter voyage number
6. Enter/select completion time
7. Submit event
8. Verify success message

### Test 10.5: Log Handling Event - UNLOAD
**Description:** Test logging an UNLOAD event for a cargo.

**Steps:**
1. Open event logger interface
2. Enter tracking ID (e.g., "JKL567")
3. Select event type: UNLOAD
4. Select location
5. Enter voyage number
6. Enter/select completion time
7. Submit event
8. Verify success message

### Test 10.6: Log Handling Event - CUSTOMS
**Description:** Test logging a CUSTOMS event for a cargo.

**Steps:**
1. Open event logger interface
2. Enter tracking ID
3. Select event type: CUSTOMS
4. Select location
5. Enter/select completion time
6. Submit event
7. Verify success message

### Test 10.7: Log Handling Event - CLAIM
**Description:** Test logging a CLAIM event for a cargo.

**Steps:**
1. Open event logger interface
2. Enter tracking ID
3. Select event type: CLAIM
4. Select location
5. Enter/select completion time
6. Submit event
7. Verify cargo status updates to claimed

### Test 10.8: Event Form Validation - Missing Tracking ID
**Description:** Test validation when tracking ID is missing.

**Steps:**
1. Open event logger interface
2. Leave tracking ID field empty
3. Fill in other fields
4. Attempt to submit
5. Verify validation error for tracking ID

### Test 10.9: Event Form Validation - Invalid Tracking ID
**Description:** Test validation with non-existent tracking ID.

**Steps:**
1. Open event logger interface
2. Enter invalid tracking ID (e.g., "INVALID999")
3. Fill in other fields
4. Submit event
5. Verify error message about invalid/not found tracking ID

### Test 10.10: Event Form Validation - Missing Event Type
**Description:** Test validation when event type is not selected.

**Steps:**
1. Open event logger interface
2. Enter valid tracking ID
3. Leave event type unselected
4. Fill in other fields
5. Attempt to submit
6. Verify validation error for event type

---

## 11. Navigation and Menu Tests

### Test 11.1: Side Menu Navigation - All Items
**Description:** Test that all side menu items are clickable and navigate correctly.

**Steps:**
1. Navigate to admin dashboard
2. Click each menu item in sequence:
   - Dashboard
   - Book
   - Track
   - Live
   - About
3. Verify each navigation works correctly
4. Verify URL changes appropriately for each

### Test 11.2: Logo Click Navigation
**Description:** Test that clicking the logo returns to home/dashboard.

**Steps:**
1. Navigate to any admin page
2. Click on Cargo Tracker logo in side panel
3. Verify navigation to dashboard or home page

### Test 11.3: Browser Back/Forward Navigation
**Description:** Test browser navigation controls work correctly.

**Steps:**
1. Navigate through several pages (home → tracking → dashboard)
2. Click browser back button
3. Verify correct page is displayed
4. Click browser forward button
5. Verify correct page is displayed

### Test 11.4: Direct URL Access
**Description:** Test that direct URL access works for all major pages.

**Steps:**
1. Navigate directly to each URL:
   - `/cargo-tracker/`
   - `/cargo-tracker/public/track.xhtml`
   - `/cargo-tracker/admin/dashboard.xhtml`
   - `/cargo-tracker/admin/show.xhtml?trackingId=ABC123`
2. Verify each page loads successfully without errors

---

## 12. Responsive Design Tests

### Test 12.1: Mobile Viewport - Home Page
**Description:** Test home page rendering on mobile viewport.

**Steps:**
1. Set browser viewport to mobile size (e.g., 375x667)
2. Navigate to home page
3. Verify layout adjusts appropriately
4. Verify all buttons are accessible
5. Verify no horizontal scrolling required

### Test 12.2: Mobile Viewport - Tracking Interface
**Description:** Test tracking interface on mobile viewport.

**Steps:**
1. Set viewport to mobile size
2. Navigate to public tracking page
3. Verify form is usable on mobile
4. Verify tracking input and button are accessible
5. Test tracking a cargo on mobile view

### Test 12.3: Mobile Viewport - Dashboard Tables
**Description:** Test dashboard cargo tables on mobile viewport.

**Steps:**
1. Set viewport to mobile size
2. Navigate to admin dashboard
3. Verify tables are responsive (scroll or stack appropriately)
4. Verify table data is readable
5. Verify links/buttons are clickable

### Test 12.4: Tablet Viewport - All Pages
**Description:** Test main pages on tablet viewport.

**Steps:**
1. Set browser viewport to tablet size (e.g., 768x1024)
2. Navigate through main pages
3. Verify layouts adjust appropriately for tablet
4. Verify side menu and main content are properly displayed

---

## 13. Error Handling and Edge Cases

### Test 13.1: Handle Network Errors
**Description:** Test application behavior when network requests fail.

**Steps:**
1. Use browser dev tools to simulate offline mode
2. Attempt to track a cargo
3. Verify appropriate error message is displayed
4. Verify application doesn't crash

### Test 13.2: Session Timeout Handling
**Description:** Test behavior when session expires (if applicable).

**Steps:**
1. Navigate to admin dashboard
2. Wait for session to timeout (or clear session cookies)
3. Attempt to perform an action
4. Verify appropriate handling (redirect, error message, etc.)

### Test 13.3: Invalid Query Parameters
**Description:** Test page behavior with invalid query parameters.

**Steps:**
1. Navigate to `/admin/show.xhtml?trackingId=INVALID`
2. Verify appropriate error handling
3. Navigate to `/admin/show.xhtml?trackingId=` (empty parameter)
4. Verify appropriate error handling

### Test 13.4: Special Characters in Input
**Description:** Test input handling with special characters.

**Steps:**
1. Navigate to tracking page
2. Enter special characters in tracking ID field: `!@#$%^&*()`
3. Submit form
4. Verify input is sanitized or error is shown appropriately

### Test 13.5: SQL Injection Prevention
**Description:** Test that SQL injection attempts are prevented.

**Steps:**
1. Navigate to tracking page
2. Enter SQL injection string: `ABC123' OR '1'='1`
3. Submit form
4. Verify input is properly sanitized and no SQL error occurs

### Test 13.6: XSS Prevention
**Description:** Test that XSS attempts are prevented.

**Steps:**
1. Navigate to tracking page
2. Enter XSS string: `<script>alert('XSS')</script>`
3. Submit form
4. Verify script is not executed and is properly escaped

---

## 14. Performance Tests

### Test 14.1: Page Load Time - Home Page
**Description:** Measure and verify home page loads within acceptable time.

**Steps:**
1. Navigate to home page
2. Measure page load time
3. Verify page loads in under 3 seconds

### Test 14.2: Page Load Time - Dashboard
**Description:** Measure and verify dashboard loads within acceptable time.

**Steps:**
1. Navigate to admin dashboard
2. Measure page load time with cargo data
3. Verify page loads in under 3 seconds

### Test 14.3: Cargo Tracking Response Time
**Description:** Measure tracking request response time.

**Steps:**
1. Navigate to tracking page
2. Enter valid tracking ID
3. Measure time from click to results display
4. Verify response time is under 2 seconds

---

## 15. Accessibility Tests

### Test 15.1: Keyboard Navigation
**Description:** Test that all functionality is accessible via keyboard.

**Steps:**
1. Navigate to home page using only Tab key
2. Verify can reach all buttons
3. Verify can activate buttons with Enter/Space
4. Test keyboard navigation through forms and menus

### Test 15.2: Screen Reader Compatibility
**Description:** Test that page structure is screen reader friendly.

**Steps:**
1. Use screen reader to navigate home page
2. Verify headings are properly structured
3. Verify form labels are associated with inputs
4. Verify table headers are properly defined

### Test 15.3: ARIA Labels
**Description:** Verify ARIA labels are present where needed.

**Steps:**
1. Inspect page elements
2. Verify buttons have aria-label attributes
3. Verify form fields have aria-required attributes
4. Verify interactive elements have appropriate ARIA attributes

### Test 15.4: Color Contrast
**Description:** Verify text has sufficient color contrast.

**Steps:**
1. Navigate through all pages
2. Verify text-to-background contrast meets WCAG standards
3. Verify links are distinguishable from regular text

---

## 16. Integration Tests

### Test 16.1: End-to-End Cargo Lifecycle
**Description:** Test complete cargo lifecycle from booking to claiming.

**Steps:**
1. Book a new cargo (origin, destination, deadline)
2. Verify cargo appears in "Not Routed" table
3. Route the cargo by selecting an itinerary
4. Verify cargo moves to "Routed" table
5. Log handling events (RECEIVE, LOAD, UNLOAD)
6. Verify events appear in cargo history
7. Log CLAIM event
8. Verify cargo moves to "Claimed" table

### Test 16.2: Cargo Tracking Through Multiple Interfaces
**Description:** Test tracking cargo from both public and admin interfaces.

**Steps:**
1. Track cargo ABC123 from public interface
2. Verify status displayed
3. Navigate to admin dashboard
4. View same cargo from admin interface
5. Verify consistent information displayed in both interfaces

### Test 16.3: Real-time Updates
**Description:** Test that cargo status updates reflect across interfaces.

**Steps:**
1. Open admin dashboard in one browser tab
2. Open event logger in another tab/window
3. Note current status of a cargo
4. Log a handling event for that cargo
5. Refresh/check dashboard
6. Verify updated status is reflected

---

## 17. Data Validation Tests

### Test 17.1: Date Format Validation
**Description:** Test that date inputs validate format correctly.

**Steps:**
1. Access booking or deadline change form
2. Enter invalid date formats
3. Attempt to submit
4. Verify validation errors for invalid formats

### Test 17.2: Past Date Validation
**Description:** Test that past dates are not accepted for deadline.

**Steps:**
1. Access booking form
2. Enter a past date as deadline
3. Attempt to submit
4. Verify validation error about past date

### Test 17.3: Location Code Validation
**Description:** Test location code validation (if editable).

**Steps:**
1. If location codes can be entered directly
2. Enter invalid location code
3. Verify validation error or dropdown prevents invalid codes

---

## 18. Browser Compatibility Tests

### Test 18.1: Chrome Compatibility
**Description:** Verify application works correctly in Chrome.

**Steps:**
1. Run key test cases in Chrome browser
2. Verify all functionality works
3. Verify UI renders correctly

### Test 18.2: Firefox Compatibility
**Description:** Verify application works correctly in Firefox.

**Steps:**
1. Run key test cases in Firefox browser
2. Verify all functionality works
3. Verify UI renders correctly

### Test 18.3: Safari Compatibility
**Description:** Verify application works correctly in Safari.

**Steps:**
1. Run key test cases in Safari browser
2. Verify all functionality works
3. Verify UI renders correctly

### Test 18.4: Edge Compatibility
**Description:** Verify application works correctly in Edge.

**Steps:**
1. Run key test cases in Edge browser
2. Verify all functionality works
3. Verify UI renders correctly

---

## Summary

**Total Test Cases:** 100+

### Test Categories:
- Home Page: 4 tests
- Public Tracking: 8 tests
- Admin Dashboard: 12 tests
- Booking: 6 tests
- Cargo Routing: 4 tests
- Cargo Details: 5 tests
- Admin Tracking: 2 tests
- Live Map: 4 tests
- About Pages: 3 tests
- Event Logger: 10 tests
- Navigation: 4 tests
- Responsive Design: 4 tests
- Error Handling: 6 tests
- Performance: 3 tests
- Accessibility: 4 tests
- Integration: 3 tests
- Data Validation: 3 tests
- Browser Compatibility: 4 tests

### Priority Levels:
- **High Priority:** Home page navigation, cargo tracking, dashboard display, booking flow, event logging
- **Medium Priority:** Routing, cargo details, map interface, form validation, responsive design
- **Low Priority:** Edge cases, accessibility, browser compatibility, performance benchmarks

### Test Data:
- **Valid Tracking IDs:** ABC123, JKL567, DEF789, MNO456
- **Sample Locations:** Hong Kong (CNHKG), Helsinki (FIHEL), Stockholm (SESTO), Melbourne (AUMEL), New York (USNYC), Dallas (USDAL), Hangzhou (CNHGH)
- **Sample Event Types:** RECEIVE, LOAD, UNLOAD, CUSTOMS, CLAIM

### Notes for Implementation:
1. Some tests may need adjustment based on actual application behavior
2. Event logger popup handling will require special Playwright context management
3. Map tests may need explicit wait for Leaflet.js library to load
4. AJAX interactions may require waiting for specific elements or network calls
5. Session management tests depend on application configuration
