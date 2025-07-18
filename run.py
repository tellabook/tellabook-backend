import os
from flask import Flask
from app.models import init_app as db_init_app
from app.routes import bp

app = Flask(__name__)

# DB config (used by init_app inside models)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db_init_app(app)

# Register blueprint
app.register_blueprint(bp, url_prefix="/")

@app.route("/")
def index():
    return "Tellabook backend is running!"

# Make sure it binds to external port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
