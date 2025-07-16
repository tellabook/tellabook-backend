import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from app.routes import bp
import os

app = Flask(__name__)
app.register_blueprint(bp, url_prefix="/")

@app.route("/")
def index():
    return "Tellabook backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
