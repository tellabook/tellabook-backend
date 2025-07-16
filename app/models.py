from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .models import Transaction  # import your models
        db.create_all()

    return app
