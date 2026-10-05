import os
from app import create_app
from app.models import db, User, Bin, Vehicle, Alert, CollectionRequest
from werkzeug.security import generate_password_hash
import datetime

app = create_app()

def seed_database():
    with app.app_context():
        db.create_all()
        
        # Check if users exist
        if User.query.first() is None:
            admin = User(username='admin', password_hash=generate_password_hash('admin123'), role='admin', name='Admin User')
            operator1 = User(username='operator', password_hash=generate_password_hash('operator123'), role='operator', name='Operator John')
            operator2 = User(username='operator2', password_hash=generate_password_hash('operator123'), role='operator', name='Operator Mike')
            operator3 = User(username='operator3', password_hash=generate_password_hash('operator123'), role='operator', name='Operator Sarah')
            db.session.add_all([admin, operator1, operator2, operator3])
            
            # Add some bins
            bins = [
                Bin(bin_id='B001', location='Central Park', area='North Zone', bin_type='General', capacity=100, fill_level=20, status='Empty'),
                Bin(bin_id='B002', location='Main Street', area='Downtown', bin_type='Recycle', capacity=120, fill_level=35, status='Normal'),
                Bin(bin_id='B003', location='University Gate', area='Campus', bin_type='General', capacity=100, fill_level=52, status='Normal'),
                Bin(bin_id='B004', location='Mall Entrance', area='Downtown', bin_type='Organic', capacity=80, fill_level=68, status='Almost Full'),
                Bin(bin_id='B005', location='Train Station', area='East Zone', bin_type='General', capacity=200, fill_level=75, status='Almost Full'),
                Bin(bin_id='B006', location='City Library', area='Downtown', bin_type='Recycle', capacity=100, fill_level=82, status='Full'),
                Bin(bin_id='B007', location='Hospital Area', area='West Zone', bin_type='Hazardous', capacity=50, fill_level=91, status='Full'),
                Bin(bin_id='B008', location='Stadium', area='South Zone', bin_type='General', capacity=500, fill_level=97, status='Overflowing'),
                Bin(bin_id='B009', location='Tech Park', area='North Zone', bin_type='E-Waste', capacity=150, fill_level=10, status='Empty'),
                Bin(bin_id='B010', location='Residential Block A', area='East Zone', bin_type='Organic', capacity=80, fill_level=100, status='Overflowing')
            ]
            db.session.add_all(bins)
            
            # Add vehicles
            v1 = Vehicle(vehicle_number='TRK-1001', vehicle_type='Compactor', capacity=5000, driver='Dave O.', status='Available')
            v2 = Vehicle(vehicle_number='TRK-1002', vehicle_type='Mini Truck', capacity=2000, driver='Pete K.', status='Assigned')
            v3 = Vehicle(vehicle_number='TRK-1003', vehicle_type='Heavy Loader', capacity=8000, driver='Steve Rogers', status='Available')
            v4 = Vehicle(vehicle_number='TRK-1004', vehicle_type='Recycle Van', capacity=1500, driver='Natasha', status='Maintenance')
            db.session.add_all([v1, v2, v3, v4])
            db.session.commit()
            
            # Add alerts
            a1 = Alert(bin_id=bins[7].id, alert_type='Overflowing', message=f'Bin {bins[7].bin_id} at {bins[7].location} is Overflowing.', priority='High', created_at=datetime.datetime.utcnow() - datetime.timedelta(hours=1))
            a2 = Alert(bin_id=bins[9].id, alert_type='Overflowing', message=f'Bin {bins[9].bin_id} at {bins[9].location} is Overflowing.', priority='High')
            a3 = Alert(bin_id=bins[6].id, alert_type='Full', message=f'Bin {bins[6].bin_id} at {bins[6].location} is Full.', priority='Medium')
            db.session.add_all([a1, a2, a3])
            
            # Add collection request
            cr1 = CollectionRequest(bin_id=bins[7].id, priority='High', status='Pending')
            cr2 = CollectionRequest(bin_id=bins[9].id, priority='High', status='Assigned', vehicle_id=v2.id, staff_id=operator1.id)
            cr3 = CollectionRequest(bin_id=bins[6].id, priority='Medium', status='Pending')
            cr4 = CollectionRequest(bin_id=bins[5].id, priority='Medium', status='In Progress', vehicle_id=v3.id, staff_id=operator2.id)
            cr5 = CollectionRequest(bin_id=bins[0].id, priority='Low', status='Completed', vehicle_id=v1.id, staff_id=operator3.id, completed_date=datetime.datetime.utcnow() - datetime.timedelta(days=1))
            db.session.add_all([cr1, cr2, cr3, cr4, cr5])
            
            db.session.commit()
            print("Database seeded successfully with demo data.")

if __name__ == '__main__':
    seed_database()
    app.run(debug=True, port=5000)
