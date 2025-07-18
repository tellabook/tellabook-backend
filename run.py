from flask import Flask
from app.models import db
from app.routes import bp
import os

try:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(bp, url_prefix="/")

    @app.route("/")
    def index():
        return "Tellabook backend is running!"

    if __name__ == "__main__":
        app.run(debug=True)
except Exception as e:
    import traceback
    print("🚨 CRITICAL ERROR IN run.py:")
    traceback.print_exc()
