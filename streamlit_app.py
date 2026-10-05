import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import datetime
import os
import sys
from werkzeug.security import check_password_hash

# Add current directory to path to allow importing Flask app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Flask app and models
from run import app, seed_database
from app.models import db, User, Bin, Vehicle, Alert, CollectionRequest

# Page config
st.set_page_config(page_title="EcoBin - Smart Waste Monitoring", page_icon="🍃", layout="wide")

# Initialize database if needed (seed_database is idempotent)
with app.app_context():
    seed_database()

# Authentication state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

# --- Helper functions (must be run in app context) ---
def get_dashboard_metrics():
    with app.app_context():
        total_bins = Bin.query.count()
        normal = Bin.query.filter(Bin.status.in_(['Empty', 'Normal'])).count()
        almost_full = Bin.query.filter_by(status='Almost Full').count()
        full_over = Bin.query.filter(Bin.status.in_(['Full', 'Overflowing'])).count()
        pending = CollectionRequest.query.filter_by(status='Pending').count()
        active = CollectionRequest.query.filter(CollectionRequest.status.in_(['Assigned', 'In Progress'])).count()
        completed = CollectionRequest.query.filter_by(status='Completed').count()
        return total_bins, normal, almost_full, full_over, pending, active, completed

def get_bins():
    with app.app_context():
        bins = Bin.query.all()
        return [{"ID": b.id, "Bin ID": b.bin_id, "Location": b.location, "Area": b.area, "Type": b.bin_type, "Capacity": b.capacity, "Fill Level": b.fill_level, "Status": b.status} for b in bins]

def simulate_sensor(bin_id):
    with app.app_context():
        b = Bin.query.get(bin_id)
        if not b: return False, "Bin not found."
        
        old_fill = b.fill_level
        increase = random.randint(5, 30)
        new_fill = min(100, b.fill_level + increase)
        
        b.fill_level = new_fill
        b.last_updated = datetime.datetime.utcnow()
        
        if 0 <= new_fill <= 30: b.status = 'Empty'
        elif 31 <= new_fill <= 60: b.status = 'Normal'
        elif 61 <= new_fill <= 80: b.status = 'Almost Full'
        elif 81 <= new_fill <= 95: b.status = 'Full'
        elif 96 <= new_fill <= 100: b.status = 'Overflowing'
        
        action_msg = ""
        if b.status in ['Full', 'Overflowing']:
            existing_alert = Alert.query.filter_by(bin_id=b.id, status='Active').first()
            if not existing_alert:
                priority = 'High' if b.status == 'Overflowing' else 'Medium'
                alert = Alert(alert_type=b.status, bin_id=b.id, message=f"Bin {b.bin_id} at {b.location} is {b.status}.", priority=priority)
                db.session.add(alert)
                action_msg += "Alert generated. "
                
                # Auto collection request
                existing_req = CollectionRequest.query.filter_by(bin_id=b.id).filter(CollectionRequest.status.in_(['Pending', 'Assigned', 'In Progress'])).first()
                if not existing_req:
                    cr = CollectionRequest(bin_id=b.id, priority='High')
                    db.session.add(cr)
                    action_msg += "High-priority collection request auto-created."
                else:
                    action_msg += f"Collection already {existing_req.status}."
        
        db.session.commit()
        return True, f"Sensor data updated successfully. Previous Fill Level: {old_fill}%. New Fill Level: {new_fill}%. Current Status: {b.status}. {action_msg}"

def update_collection_status(req_id, new_status, v_id=None, s_id=None):
    with app.app_context():
        cr = CollectionRequest.query.get(req_id)
        if not cr: return False
        
        if v_id: cr.vehicle_id = v_id
        if s_id: cr.staff_id = s_id
        
        cr.status = new_status
        if new_status == 'Assigned' and cr.vehicle:
            cr.vehicle.status = 'Assigned'
            
        if new_status == 'Completed':
            cr.completed_date = datetime.datetime.utcnow()
            if cr.bin:
                cr.bin.fill_level = 0
                cr.bin.status = 'Empty'
                cr.bin.last_updated = datetime.datetime.utcnow()
                for alert in Alert.query.filter_by(bin_id=cr.bin_id, status='Active').all():
                    alert.status = 'Resolved'
            if cr.vehicle:
                cr.vehicle.status = 'Available'
                
        db.session.commit()
        return True

# --- Login View ---
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center;'>🍃 EcoBin - Smart Waste Monitoring</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Login to access the system</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                with app.app_context():
                    user = User.query.filter_by(username=username).first()
                    if user and check_password_hash(user.password_hash, password):
                        st.session_state['logged_in'] = True
                        st.session_state['user'] = {'id': user.id, 'name': user.name, 'role': user.role}
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        st.info("**Demo Credentials:**\n\nAdmin: `admin` / `admin123`\n\nOperator: `operator` / `operator123`")
    st.stop()

# --- Main App ---
st.sidebar.title(f"🍃 EcoBin")
st.sidebar.markdown(f"**Welcome, {st.session_state['user']['name']}** ({st.session_state['user']['role'].capitalize()})")
st.sidebar.markdown("---")

pages = ["Dashboard", "Waste Bins", "Alerts", "Collections", "Vehicles", "Analytics", "Incremental Development", "About Project"]
selection = st.sidebar.radio("Navigation", pages)
st.sidebar.markdown("---")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state['logged_in'] = False
    st.rerun()

# 1. Dashboard
if selection == "Dashboard":
    st.title("System Dashboard")
    total, normal, almost_full, full_over, pending, active, completed = get_dashboard_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Bins", total)
    col2.metric("Normal / Empty", normal)
    col3.metric("Almost Full", almost_full)
    col4.metric("Full / Overflowing", full_over, delta_color="inverse")
    
    col5, col6, col7 = st.columns(3)
    col5.metric("Pending Collections", pending)
    col6.metric("Active Collections", active)
    col7.metric("Completed Collections", completed)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Bin Status Distribution")
        df_bins = pd.DataFrame(get_bins())
        if not df_bins.empty:
            fig1 = px.pie(df_bins, names='Status', color='Status', 
                          color_discrete_map={'Empty':'gray', 'Normal':'green', 'Almost Full':'orange', 'Full':'red', 'Overflowing':'darkred'})
            st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.subheader("Recent Alerts")
        with app.app_context():
            alerts = Alert.query.filter_by(status='Active').order_by(Alert.created_at.desc()).limit(5).all()
            if alerts:
                for a in alerts:
                    st.warning(f"**{a.alert_type}** (Bin {a.bin.bin_id}) - {a.message} [{a.created_at.strftime('%H:%M')}]")
            else:
                st.success("No active alerts.")

# 2. Waste Bins
elif selection == "Waste Bins":
    st.title("Waste Bins Management")
    
    c1, c2, c3 = st.columns([2, 1, 1])
    search = c1.text_input("Search Location or ID")
    df_bins = pd.DataFrame(get_bins())
    
    if not df_bins.empty:
        status_filter = c2.selectbox("Filter Status", ["All"] + list(df_bins['Status'].unique()))
        area_filter = c3.selectbox("Filter Area", ["All"] + list(df_bins['Area'].unique()))
        
        if search: df_bins = df_bins[df_bins['Location'].str.contains(search, case=False) | df_bins['Bin ID'].str.contains(search, case=False)]
        if status_filter != "All": df_bins = df_bins[df_bins['Status'] == status_filter]
        if area_filter != "All": df_bins = df_bins[df_bins['Area'] == area_filter]
        
        st.dataframe(df_bins, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Bin Details & Sensor Simulation")
        selected_bin_id = st.selectbox("Select Bin to View/Simulate", df_bins['ID'].tolist(), format_func=lambda x: df_bins[df_bins['ID']==x]['Bin ID'].values[0] + " - " + df_bins[df_bins['ID']==x]['Location'].values[0])
        
        if selected_bin_id:
            bin_data = df_bins[df_bins['ID'] == selected_bin_id].iloc[0]
            st.write(f"**Current Fill Level:** {bin_data['Fill Level']}% ({bin_data['Status']})")
            st.progress(bin_data['Fill Level'] / 100)
            
            if st.button("📡 Simulate Sensor Update", type="primary"):
                success, msg = simulate_sensor(selected_bin_id)
                if success:
                    st.success(msg)
                    st.rerun()

# 3. Alerts
elif selection == "Alerts":
    st.title("System Alerts")
    with app.app_context():
        alerts = Alert.query.filter_by(status='Active').all()
        if not alerts:
            st.success("No active alerts.")
        else:
            for a in alerts:
                with st.container():
                    st.warning(f"🚨 **{a.alert_type}** | Bin {a.bin.bin_id} | {a.priority} Priority")
                    st.write(f"**Location:** {a.bin.location} | **Time:** {a.created_at.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"{a.message}")
                    if st.button(f"Resolve Alert #{a.id}", key=f"res_{a.id}"):
                        a.status = 'Resolved'
                        db.session.commit()
                        st.success("Alert resolved.")
                        st.rerun()
                    st.markdown("---")

# 4. Collections
elif selection == "Collections":
    st.title("Collection Management")
    with app.app_context():
        reqs = CollectionRequest.query.order_by(CollectionRequest.request_date.desc()).all()
        if not reqs:
            st.info("No collection requests.")
        else:
            for r in reqs:
                with st.expander(f"Request #{r.id} - Bin {r.bin.bin_id} ({r.status}) - {r.priority} Priority", expanded=(r.status!='Completed')):
                    st.write(f"**Location:** {r.bin.location} | **Current Bin Fill:** {r.bin.fill_level}%")
                    if r.vehicle and r.staff:
                        st.write(f"**Assigned:** {r.vehicle.vehicle_number} / {r.staff.name}")
                    
                    if r.status == 'Pending' and st.session_state['user']['role'] == 'admin':
                        st.write("**Assign Vehicle & Staff**")
                        c1, c2, c3 = st.columns(3)
                        avail_vehicles = Vehicle.query.filter_by(status='Available').all()
                        avail_staff = User.query.filter_by(role='operator').all()
                        v_sel = c1.selectbox("Vehicle", [v.id for v in avail_vehicles], format_func=lambda x: [v.vehicle_number for v in avail_vehicles if v.id==x][0] if avail_vehicles else "", key=f"v_{r.id}")
                        s_sel = c2.selectbox("Staff", [s.id for s in avail_staff], format_func=lambda x: [s.name for s in avail_staff if s.id==x][0] if avail_staff else "", key=f"s_{r.id}")
                        if c3.button("Assign", key=f"btn_assign_{r.id}"):
                            if v_sel and s_sel:
                                update_collection_status(r.id, 'Assigned', v_sel, s_sel)
                                st.success("Assigned successfully.")
                                st.rerun()
                            else:
                                st.error("Select both vehicle and staff.")
                    elif r.status in ['Assigned', 'In Progress']:
                        c1, c2 = st.columns(2)
                        new_status = c1.selectbox("Update Status", ["In Progress", "Completed"] if r.status == "Assigned" else ["Completed"], key=f"stat_{r.id}")
                        if c2.button("Update Status", key=f"btn_stat_{r.id}"):
                            update_collection_status(r.id, new_status)
                            st.success(f"Status updated to {new_status}.")
                            if new_status == 'Completed':
                                st.info("Bin fill level reset to 0% and alerts resolved.")
                            st.rerun()

# 5. Vehicles
elif selection == "Vehicles":
    st.title("Vehicle Fleet")
    with app.app_context():
        vehicles = Vehicle.query.all()
        v_data = [{"Number": v.vehicle_number, "Type": v.vehicle_type, "Capacity": f"{v.capacity}L", "Driver": v.driver, "Status": v.status} for v in vehicles]
        st.dataframe(pd.DataFrame(v_data), use_container_width=True, hide_index=True)

# 6. Analytics
elif selection == "Analytics":
    st.title("System Analytics")
    with app.app_context():
        avg_fill = db.session.query(db.func.avg(Bin.fill_level)).scalar() or 0
        total_colls = CollectionRequest.query.count()
        completed = CollectionRequest.query.filter_by(status='Completed').count()
        completion_rate = (completed / total_colls * 100) if total_colls > 0 else 0
        overflows = Alert.query.filter_by(alert_type='Overflowing').count()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg Fill Level", f"{avg_fill:.1f}%")
        c2.metric("Completion Rate", f"{completion_rate:.1f}%")
        c3.metric("Total Overflows", overflows)
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            reqs = CollectionRequest.query.all()
            req_data = [{"Status": r.status} for r in reqs]
            if req_data:
                df = pd.DataFrame(req_data)
                fig = px.histogram(df, x="Status", title="Collection Requests by Status", color="Status")
                st.plotly_chart(fig, use_container_width=True)
                
        with c2:
            bins = Bin.query.all()
            bin_data = [{"Area": b.area, "Fill Level": b.fill_level} for b in bins]
            if bin_data:
                df = pd.DataFrame(bin_data)
                fig = px.box(df, x="Area", y="Fill Level", title="Fill Level by Area")
                st.plotly_chart(fig, use_container_width=True)

# 7. Incremental Development
elif selection == "Incremental Development":
    st.title("Incremental Development Model")
    st.markdown("""
    <div style='background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
    <strong>Software Engineering Concept:</strong><br>
    Instead of developing the complete system at once, the system was developed and delivered in functional increments. Each increment added usable functionality to the previous version, allowing for easier testing, debugging, and continuous improvement.
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Increment 1: Foundation (Basic Management)")
    st.info("**Objective:** Establish infrastructure and basic operations for waste bins.\n\n**Result:** Admin login, database schema, and bin CRUD functionality.")
    
    st.subheader("Increment 2: Smart Logic (Smart Monitoring)")
    st.warning("**Objective:** Introduce simulated IoT sensor capabilities.\n\n**Result:** Automated dynamic fill level calculation, threshold logic, and automated alert generation.")
    
    st.subheader("Increment 3: Operations (Collection Management)")
    st.success("**Objective:** Enable actionable responses to the sensor data.\n\n**Result:** Create collection requests, dispatch trucks, and auto-reset bins upon task completion.")
    
    st.subheader("Increment 4: Data Insights (Analytics)")
    st.error("**Objective:** Provide a high-level view of system performance.\n\n**Result:** Dashboard charts, fill-level distributions, and system metrics.")
    
    st.subheader("Increment 5: Smart Automation (Polish)")
    st.info("**Objective:** Introduce automated decision-making.\n\n**Result:** When a bin overflows during simulation, the system prevents duplicate tasks and automatically spawns a high-priority dispatch.")

# 8. About Project
elif selection == "About Project":
    st.title("About Project")
    st.markdown("""
    ### Smart Waste Collection Monitoring System
    
    **Development Model:** Incremental Development Model  
    **Course:** Software Engineering Practices
    
    ---
    
    ### SDG Alignment
    
    🌍 **SDG 9 – Industry, Innovation and Infrastructure**  
    This project supports this goal by demonstrating a technology-driven, scalable software solution to modernize municipal waste management operations through innovative simulated IoT integrations.
    
    🏙️ **SDG 11 – Sustainable Cities and Communities**  
    By optimizing waste collection routes and preventing overflowing bins, the system directly contributes to creating cleaner, healthier, and more sustainable urban environments.
    """)
