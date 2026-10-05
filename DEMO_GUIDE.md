# Video Demonstration Script

Use this exact script to structure your 5–7 minute video presentation. Practice it a few times to ensure smooth transitions between pages.

### Preparation Before Recording
- Ensure the app is running (`python run.py`).
- Have the login page open in your browser (`http://127.0.0.1:5000`).
- Ensure the database is freshly seeded.

---

### [0:00 – 0:30] Introduction
**(Action: Leave screen on the Login page)**
**Say:** "Hello, my name is [Your Name]. For my Software Engineering Practices micro-project, I have developed a Smart Waste Collection Monitoring System. Traditional waste collection relies on static routes, meaning trucks waste fuel visiting empty bins while missing overflowing ones in busy areas. My project solves this by using simulated IoT sensor data to route trucks dynamically based on actual need."

### [0:30 – 1:00] Project Objective & Incremental Model
**(Action: Log in using `admin` / `admin123`)**
**Say:** "As per my assigned topic, I built this entire system strictly following the Incremental Development Model. Instead of building everything at once, I delivered the project in five functional increments, ensuring stability at each step. Let me show you how it works."

### [1:00 – 2:00] Dashboard and Bins (Increment 1)
**(Action: Show the Dashboard charts, then click 'Waste Bins' on the sidebar)**
**Say:** "This is the result of Increment 1—the foundational dashboard and bin management module. As an administrator, I have a complete view of all waste bins across the city. You can see their locations, capacities, and visual progress bars representing their current fill levels."

### [2:00 – 3:00] Sensor Simulation (Increment 2)
**(Action: Click the 'Eye' icon on a bin that is currently Empty/Normal, e.g., B001)**
**Say:** "Because this is a software prototype without physical hardware, Increment 2 focused on smart logic simulation. I built a simulation tool to represent IoT sensor data. Watch what happens when I click 'Simulate Sensor Update'."
**(Action: Click the simulate button 2 or 3 times until it reaches 'Almost Full' or 'Full')**
**Say:** "The system automatically recalculates the fill percentage and categorizes the status. As you can see, the new fill level and status are clearly displayed."

### [3:00 – 4:00] Automatic Alert & Request (Increment 5)
**(Action: Click simulate again until the bin hits >95% Overflowing)**
**Say:** "Now the bin has reached critical levels. Notice the flash message. Increment 5 introduced an automated smart feature: the system immediately generated a High Priority Alert, and it automatically dispatched a Pending Collection Request without requiring human intervention. Let's look at the Alerts page."
**(Action: Click 'Alerts', show the active alert. Then click 'Collections')**
**Say:** "Here in the Collection Management module—which was Increment 3—we see the auto-generated high-priority request."

### [4:00 – 5:00] Vehicle Assignment & Completion (Increment 3)
**(Action: Click 'Assign', select a vehicle and staff, and save. Then click 'Update Status', select 'Completed', and save.)**
**Say:** "I will assign a vehicle and an operator to this request. The operator goes out and collects the waste. Once they mark the job as 'Completed' in the system, look what happens to the bin..."
**(Action: Navigate quickly back to the 'Waste Bins' list)**
**Say:** "The system automatically resets the bin's fill level back to 0% and clears all associated alerts. The lifecycle is complete."

### [5:00 – 6:00] Analytics (Increment 4)
**(Action: Click 'Analytics' on the sidebar)**
**Say:** "Increment 4 focused on data insights. This Analytics page uses Chart.js to process the live database information into visual reports, showing the distribution of bin statuses and average fill levels across the smart city."

### [6:00 – 7:00] Incremental Development & Conclusion
**(Action: Click 'Incremental Dev' on the sidebar)**
**Say:** "To clearly demonstrate my Software Engineering topic, I created this timeline page. It visually maps out how I built the system: starting from basic CRUD in Increment 1, adding smart logic in Increment 2, building operational tools in Increment 3, data charts in Increment 4, and finally automation in Increment 5."
**(Action: Click 'About Project' on the sidebar)**
**Say:** "In conclusion, this project directly supports SDG 9 (Innovation and Infrastructure) and SDG 11 (Sustainable Cities). By applying the Incremental Development Model, I was able to build a robust, scalable prototype that modernizes municipal waste management. Thank you."
