from app import db
from flask_login import UserMixin
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='operator') # admin or operator
    name = db.Column(db.String(100))

class Bin(db.Model):
    __tablename__ = 'bins'
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100))
    bin_type = db.Column(db.String(50))
    capacity = db.Column(db.Integer, default=100) # in liters or kg
    fill_level = db.Column(db.Integer, default=0) # 0 to 100 percentage
    status = db.Column(db.String(20), default='Empty') # Empty, Normal, Almost Full, Full, Overflowing
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    alerts = db.relationship('Alert', backref='bin', lazy=True, cascade="all, delete-orphan")
    collection_requests = db.relationship('CollectionRequest', backref='bin', lazy=True, cascade="all, delete-orphan")

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    driver = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Available') # Available, Assigned, On Route, Maintenance
    
    collection_requests = db.relationship('CollectionRequest', backref='vehicle', lazy=True)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    bin_id = db.Column(db.Integer, db.ForeignKey('bins.id'), nullable=False)
    message = db.Column(db.String(255))
    priority = db.Column(db.String(20), default='Medium') # Low, Medium, High
    status = db.Column(db.String(20), default='Active') # Active, Resolved
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class CollectionRequest(db.Model):
    __tablename__ = 'collection_requests'
    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.Integer, db.ForeignKey('bins.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(20), default='Pending') # Pending, Assigned, In Progress, Completed
    priority = db.Column(db.String(20), default='Normal')
    request_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    scheduled_date = db.Column(db.DateTime, nullable=True)
    completed_date = db.Column(db.DateTime, nullable=True)
    
    staff = db.relationship('User', backref='assigned_collections')
