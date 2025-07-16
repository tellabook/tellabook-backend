from flask import Flask
from app.routes import bp
from app.models import init_app

app = Flask(__name__)
init_app(app)

app.register_blueprint(bp, url_prefix="/")

@app.route("/")
def index():
    return "Tellabook backend is running!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
