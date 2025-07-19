from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(120), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=True)
    invoice_date = db.Column(db.Date, nullable=True)
    invoice_number = db.Column(db.String(50), nullable=True)
    terms = db.Column(db.String(80), nullable=True)
    tags = db.Column(db.String(255), nullable=True)  # comma-separated tags
    memo = db.Column(db.Text, nullable=True)
    fixed_asset_account = db.Column(db.String(120), nullable=True)
    inventory_account = db.Column(db.String(120), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="staged")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserCommandHistory(db.Model):
    __tablename__ = 'user_command_history'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
