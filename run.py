from flask import Flask
from app.routes import bp
from app.models import init_app as db_init_app

app = Flask(__name__)
db_init_app(app)

app.register_blueprint(bp, url_prefix="/")

@app.route("/")
def index():
    return "Tellabook backend is running!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

