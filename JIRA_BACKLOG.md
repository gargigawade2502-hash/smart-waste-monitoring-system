# Agile Backlog (JIRA Format)

This file simulates a JIRA project backlog for the Incremental Development Model.

## Suggested Sprint Structure
- **Sprint 1:** Project setup + authentication + basic bin management (Increment 1)
- **Sprint 2:** Smart monitoring + sensor simulation + alerts (Increment 2)
- **Sprint 3:** Collection + vehicle management (Increment 3)
- **Sprint 4:** Analytics + optimization (Increment 4 & 5)
- **Sprint 5:** Documentation + final testing + presentation prep

## Epics & User Stories

### EPIC 1: Increment 1 - Basic Waste Bin Management
**Priority:** High
| Task ID | Title | Description | Story Points | Status |
|---|---|---|---|---|
| SWM-01 | Setup Flask Environment | Initialize project, configure SQLite, create folder structure. | 3 | Done |
| SWM-02 | User Authentication | Implement login/logout functionality and user roles. | 3 | Done |
| SWM-03 | Base Dashboard Layout | Create responsive sidebar and top nav using Bootstrap. | 2 | Done |
| SWM-04 | Bin Database Model | Create Bin table with location, type, capacity. | 2 | Done |
| SWM-05 | Bin CRUD Operations | Implement add, view, edit, delete functionality for bins. | 5 | Done |

### EPIC 2: Increment 2 - Smart Monitoring
**Priority:** High
| Task ID | Title | Description | Story Points | Status |
|---|---|---|---|---|
| SWM-06 | Sensor Simulation | Create a button/route to randomly increment bin fill level. | 3 | Done |
| SWM-07 | Threshold Logic | Write logic to map percentage (0-100) to status (Normal, Full, etc.). | 2 | Done |
| SWM-08 | Visual Indicators | Update UI to show progress bars changing color based on level. | 2 | Done |
| SWM-09 | Alert Generation | Auto-create an Alert record when bin reaches 80%+. | 3 | Done |
| SWM-10 | Alerts UI | Create a page to view and resolve active alerts. | 3 | Done |

### EPIC 3: Increment 3 - Collection Management
**Priority:** Medium
| Task ID | Title | Description | Story Points | Status |
|---|---|---|---|---|
| SWM-11 | Vehicle Database Model | Create Vehicle table and basic viewing UI. | 2 | Done |
| SWM-12 | Collection Request Model | Create table to link bin, vehicle, staff, and status. | 2 | Done |
| SWM-13 | Assignment UI | Allow admin to select a vehicle and staff for a pending request. | 5 | Done |
| SWM-14 | Status Tracking | Allow updating status from Pending -> In Progress -> Completed. | 3 | Done |
| SWM-15 | Completion Trigger | When completed, automatically reset bin fill level to 0%. | 2 | Done |

### EPIC 4: Increment 4 - Analytics and Reporting
**Priority:** Medium
| Task ID | Title | Description | Story Points | Status |
|---|---|---|---|---|
| SWM-16 | Dashboard Metrics | Calculate and display total bins, active collections, etc. | 3 | Done |
| SWM-17 | Chart.js Integration | Add bar chart to dashboard showing bin status distribution. | 3 | Done |
| SWM-18 | Analytics Page | Create dedicated analytics view with overall system averages. | 3 | Done |

### EPIC 5: Increment 5 - Optimization / Smart Feature
**Priority:** Low
| Task ID | Title | Description | Story Points | Status |
|---|---|---|---|---|
| SWM-19 | Auto-Collection Trigger | When a bin triggers an overflow alert, auto-create a pending collection request. | 3 | Done |
| SWM-20 | Incremental Dev Page | Build a UI page mapping out the project's evolution step-by-step. | 2 | Done |

### EPIC 6: Testing & Documentation
**Priority:** High
| Task ID | Title | Description | Story Points | Status |
|---|---|---|---|---|
| SWM-21 | System Testing | Execute 15 documented test cases covering main flows. | 5 | Done |
| SWM-22 | Project Report Content | Generate textual content for the college submission report. | 3 | Done |
| SWM-23 | Presentation Outline | Create slide structures for final demo. | 2 | Done |
