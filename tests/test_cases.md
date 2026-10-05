# Test Cases

## Summary
These 15 test cases cover the core functionality of the Incremental Smart Waste Monitoring System.

| TC ID | Test Scenario | Precondition | Test Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC01 | Valid Admin Login | User is on login page | User: admin, Pass: admin123 | Redirected to Dashboard with admin privileges. | System redirected to dashboard, username displayed. | Pass |
| TC02 | Invalid Login | User is on login page | User: wrong, Pass: wrong | "Invalid username or password" flash message shown. | Flash message appeared, login rejected. | Pass |
| TC03 | Add New Bin | Admin is logged in | ID: B015, Type: General | Bin is saved to database and appears in bin list. | Bin saved, visible in table with 0% fill. | Pass |
| TC04 | View Bin Details | Bins exist in system | Click "Eye" icon on a bin | Bin details page opens showing capacity and fill level. | Details rendered correctly. | Pass |
| TC05 | Delete Bin | Admin is logged in | Click "Trash" icon (Admin only) | Bin is removed from the database and UI list. | Bin deleted from database successfully. | Pass |
| TC06 | Simulate Sensor - Low | Bin fill level is < 20% | Click "Simulate" | Status updates to "Normal". Progress bar turns green. | Fill level updated to 35%, status changed to Normal. | Pass |
| TC07 | Simulate Sensor - High | Bin fill level is 70% | Click "Simulate" | Status updates to "Full" or "Overflowing". | Fill level reached 95%, status changed to Full. | Pass |
| TC08 | Automatic Alert Gen | Bin reaches >80% capacity | Sensor simulation pushes bin to 85% | Alert is created and visible on the Dashboard & Alerts page. | Alert generated successfully. | Pass |
| TC09 | Resolve Alert | Active alert exists | Click "Resolve" on active alert | Alert status changes to Resolved and moves to history. | Moved to resolved list. | Pass |
| TC10 | Auto-Create Request | Bin triggers overflow alert | Sensor pushes bin to 98% | A pending high-priority collection request is automatically generated. | Request auto-created and visible in Collections. | Pass |
| TC11 | Prevent Dup Request | Bin is at 98% (Already Pending) | Click "Simulate" again | System detects existing pending request, does NOT create a duplicate. | "Collection already Pending" message shown. | Pass |
| TC12 | Assign Vehicle | Pending request exists | Select vehicle TRK-1001 and operator | Collection status changes to 'Assigned'. | Status updated to Assigned. | Pass |
| TC13 | Invalid Assignment | Pending request exists | Submit without selecting vehicle | System rejects assignment and shows error message. | HTML5 validation blocked submission. | Pass |
| TC14 | Complete Collection | Request is In Progress | Change status to "Completed" | Bin fill level drops to 0%. Related alerts are resolved. | Bin reset to 0% Empty, alert marked Resolved. | Pass |
| TC15 | Analytics Update | Request is completed | Navigate to Analytics page | Total completed collections metric increases by 1. | Number incremented accurately on dashboard. | Pass |
