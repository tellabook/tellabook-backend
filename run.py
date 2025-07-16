from flask import Flask
from app.routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
