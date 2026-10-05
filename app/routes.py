from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db, User, Bin, Vehicle, Alert, CollectionRequest
import datetime
import random

main = Blueprint('main', __name__)

@main.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    total_bins = Bin.query.count()
    normal_bins = Bin.query.filter(Bin.status.in_(['Empty', 'Normal'])).count()
    almost_full_bins = Bin.query.filter_by(status='Almost Full').count()
    full_overflowing_bins = Bin.query.filter(Bin.status.in_(['Full', 'Overflowing'])).count()
    
    pending_collections = CollectionRequest.query.filter_by(status='Pending').count()
    active_collections = CollectionRequest.query.filter(CollectionRequest.status.in_(['Assigned', 'In Progress'])).count()
    completed_collections = CollectionRequest.query.filter_by(status='Completed').count()
    
    alerts = Alert.query.filter_by(status='Active').order_by(Alert.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                           total_bins=total_bins, normal_bins=normal_bins, 
                           almost_full_bins=almost_full_bins, full_overflowing_bins=full_overflowing_bins,
                           pending_collections=pending_collections, active_collections=active_collections,
                           completed_collections=completed_collections,
                           alerts=alerts)

# --- Bins ---
@main.route('/bins')
@login_required
def bins():
    all_bins = Bin.query.all()
    return render_template('bins.html', bins=all_bins)

@main.route('/bin/add', methods=['GET', 'POST'])
@login_required
def add_bin():
    if request.method == 'POST':
        bin_id = request.form.get('bin_id')
        location = request.form.get('location')
        area = request.form.get('area')
        bin_type = request.form.get('bin_type')
        capacity = request.form.get('capacity', type=int)
        
        new_bin = Bin(bin_id=bin_id, location=location, area=area, bin_type=bin_type, capacity=capacity)
        db.session.add(new_bin)
        db.session.commit()
        flash('Waste bin added successfully.', 'success')
        return redirect(url_for('main.bins'))
    return render_template('add_bin.html')

@main.route('/bin/<int:id>')
@login_required
def bin_details(id):
    b = Bin.query.get_or_404(id)
    return render_template('bin_details.html', bin=b)

@main.route('/bin/<int:id>/delete')
@login_required
def delete_bin(id):
    if current_user.role != 'admin':
        flash('Unauthorized.', 'danger')
        return redirect(url_for('main.bins'))
    b = Bin.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    flash('Bin deleted.', 'info')
    return redirect(url_for('main.bins'))

# --- Smart Sensor Simulation ---
@main.route('/simulate_sensor/<int:id>', methods=['POST'])
@login_required
def simulate_sensor(id):
    b = Bin.query.get_or_404(id)
    # Simulate a fill level increase between 5 and 30 percent
    increase = random.randint(5, 30)
    old_fill_level = b.fill_level
    new_fill_level = min(100, b.fill_level + increase)
    
    b.fill_level = new_fill_level
    b.last_updated = datetime.datetime.utcnow()
    
    # Calculate status based on rules
    if 0 <= new_fill_level <= 30:
        b.status = 'Empty'
    elif 31 <= new_fill_level <= 60:
        b.status = 'Normal'
    elif 61 <= new_fill_level <= 80:
        b.status = 'Almost Full'
    elif 81 <= new_fill_level <= 95:
        b.status = 'Full'
    elif 96 <= new_fill_level <= 100:
        b.status = 'Overflowing'
        
    action_message = ""
    # Generate alert if required
    if b.status in ['Full', 'Overflowing']:
        existing_alert = Alert.query.filter_by(bin_id=b.id, status='Active').first()
        if not existing_alert:
            priority = 'High' if b.status == 'Overflowing' else 'Medium'
            alert = Alert(alert_type=b.status, bin_id=b.id, message=f"Bin {b.bin_id} at {b.location} is {b.status}.", priority=priority)
            db.session.add(alert)
            action_message = f"Alert generated."
            
            # Simple intelligent feature (Increment 5): Auto-create collection request
            existing_request = CollectionRequest.query.filter_by(bin_id=b.id).filter(CollectionRequest.status.in_(['Pending', 'Assigned', 'In Progress'])).first()
            if not existing_request:
                cr = CollectionRequest(bin_id=b.id, priority='High')
                db.session.add(cr)
                action_message += f" High-priority collection request auto-created."
            else:
                action_message += f" Collection already {existing_request.status}."
                
    db.session.commit()
    flash(f'Sensor data updated successfully. Previous Fill Level: {old_fill_level}%. New Fill Level: {new_fill_level}%. Current Status: {b.status}. {action_message}', 'success')
    return redirect(url_for('main.bin_details', id=b.id))

# --- Alerts ---
@main.route('/alerts')
@login_required
def alerts():
    active_alerts = Alert.query.filter_by(status='Active').order_by(Alert.created_at.desc()).all()
    resolved_alerts = Alert.query.filter_by(status='Resolved').order_by(Alert.created_at.desc()).limit(20).all()
    return render_template('alerts.html', active_alerts=active_alerts, resolved_alerts=resolved_alerts)

@main.route('/alert/<int:id>/resolve')
@login_required
def resolve_alert(id):
    a = Alert.query.get_or_404(id)
    a.status = 'Resolved'
    db.session.commit()
    flash('Alert marked as resolved.', 'success')
    return redirect(url_for('main.alerts'))

# --- Collection Management ---
@main.route('/collections')
@login_required
def collections():
    reqs = CollectionRequest.query.order_by(CollectionRequest.request_date.desc()).all()
    vehicles = Vehicle.query.filter_by(status='Available').all()
    staff = User.query.filter_by(role='operator').all()
    return render_template('collections.html', requests=reqs, vehicles=vehicles, staff=staff)

@main.route('/collection/<int:id>/assign', methods=['POST'])
@login_required
def assign_collection(id):
    cr = CollectionRequest.query.get_or_404(id)
    vehicle_id = request.form.get('vehicle_id')
    staff_id = request.form.get('staff_id')
    
    if vehicle_id and staff_id:
        cr.vehicle_id = vehicle_id
        cr.staff_id = staff_id
        cr.status = 'Assigned'
        
        v = Vehicle.query.get(vehicle_id)
        if v:
            v.status = 'Assigned'
            
        db.session.commit()
        flash('Collection request assigned successfully.', 'success')
    else:
        flash('Please select both vehicle and staff.', 'danger')
        
    return redirect(url_for('main.collections'))

@main.route('/collection/<int:id>/update_status', methods=['POST'])
@login_required
def update_collection_status(id):
    cr = CollectionRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    
    cr.status = new_status
    if new_status == 'Completed':
        cr.completed_date = datetime.datetime.utcnow()
        # Reset the bin
        if cr.bin:
            cr.bin.fill_level = 0
            cr.bin.status = 'Empty'
            cr.bin.last_updated = datetime.datetime.utcnow()
            # Resolve related alerts
            for alert in Alert.query.filter_by(bin_id=cr.bin_id, status='Active').all():
                alert.status = 'Resolved'
        # Release the vehicle
        if cr.vehicle:
            cr.vehicle.status = 'Available'
            
    db.session.commit()
    flash('Collection status updated.', 'success')
    return redirect(url_for('main.collections'))

# --- Vehicles ---
@main.route('/vehicles')
@login_required
def vehicles():
    all_vehicles = Vehicle.query.all()
    return render_template('vehicles.html', vehicles=all_vehicles)

# --- Analytics ---
@main.route('/analytics')
@login_required
def analytics():
    # Simple analytics data for college presentation
    total_bins = Bin.query.count()
    if total_bins > 0:
        avg_fill = db.session.query(db.func.avg(Bin.fill_level)).scalar() or 0
    else:
        avg_fill = 0
        
    completed_colls = CollectionRequest.query.filter_by(status='Completed').count()
    overflow_incidents = Alert.query.filter_by(alert_type='Overflowing').count()
    
    # Fill level distribution for chart
    fill_data = {
        'Empty': Bin.query.filter_by(status='Empty').count(),
        'Normal': Bin.query.filter_by(status='Normal').count(),
        'Almost Full': Bin.query.filter_by(status='Almost Full').count(),
        'Full': Bin.query.filter_by(status='Full').count(),
        'Overflowing': Bin.query.filter_by(status='Overflowing').count()
    }
    
    return render_template('analytics.html', avg_fill=round(avg_fill, 1), 
                           completed_colls=completed_colls, overflow_incidents=overflow_incidents,
                           fill_data=fill_data)

# --- Info Pages ---
@main.route('/incremental_development')
def incremental_development():
    return render_template('incremental_development.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

