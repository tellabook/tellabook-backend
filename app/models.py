from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy.dialects.postgresql import JSON

# Initialize DB object
db = SQLAlchemy()

# ========== MODELS ==========

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(120), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=True)
    invoice_date = db.Column(db.Date, nullable=True)
    invoice_number = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="staged")  # staged, confirmed, posted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    taxes = db.Column(JSON, nullable=True)  # ✅ Added taxes as JSON field

class UserCommandHistory(db.Model):
    __tablename__ = 'user_command_history'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    output_summary = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    default_category = db.Column(db.String(80), nullable=True)

# ========== INITIALIZATION ==========

def init_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
