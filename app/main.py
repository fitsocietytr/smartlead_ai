from flask import Flask, render_template
from flask_cors import CORS

from app.routes import pages_bp, api_bp

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(pages_bp)
app.register_blueprint(api_bp)

@app.route("/")
def ana_sayfa():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)