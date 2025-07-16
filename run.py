from flask import Flask
from app.routes import bp
import os

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
