# Smart Waste Collection Monitoring System

## Overview
This is a micro-project developed for the Software Engineering Practices (SEP) course. It demonstrates the **Incremental Development Model** applied to a Smart Waste Collection System, aligning with SDG 9 (Industry, Innovation, and Infrastructure).

## Features
- **Dashboard:** Real-time metrics and charts.
- **Waste Bin Management:** Add, view, edit, delete bins.
- **Smart Sensor Simulation:** Simulates IoT sensor data updating bin fill levels.
- **Automated Alerts:** Generates alerts when bins become full or overflowing.
- **Collection Management:** Assign vehicles and staff to collection requests.
- **Analytics:** Visualize system performance.
- **Incremental Development View:** A dedicated page explaining the project's evolution.

## Technology Stack
- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome
- **Database:** SQLite (via SQLAlchemy)
- **Data Visualization:** Chart.js

## Setup Instructions

1. **Prerequisites:** Make sure you have Python 3 installed.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 1. LOCAL FLASK VERSION
To run the traditional web application version:
```bash
python run.py
```
*Note: Running `run.py` for the first time will automatically create the SQLite database and seed it with demo data.*
Access the application: Open your browser and go to `http://127.0.0.1:5000`

### 2. STREAMLIT VERSION (Cloud Ready)
To run the modern interactive dashboard version locally:
```bash
streamlit run streamlit_app.py
```
*Note: This version uses the same SQLite database. It is designed to be easily deployable on Streamlit Community Cloud.*

## Deployment via Streamlit Community Cloud
1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Deploy the app by selecting `streamlit_app.py` as the main file.
4. (Optional) Set up secrets in the Streamlit dashboard based on `.streamlit/secrets.toml.example`.

## Demo Credentials
- **Admin Role:**
  - Username: `admin`
  - Password: `admin123`
- **Operator Role:**
  - Username: `operator`
  - Password: `operator123`

## Project Structure
- `app/`: Contains the Flask application, templates, and static assets.
- `database/`: Contains the SQLite database file.
- `docs/`: Contains Mermaid diagrams and other documentation.
- `reports/`: Contains content for the final report and presentation.
- `tests/`: Contains test case documentation.
