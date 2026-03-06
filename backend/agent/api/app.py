from flask import Flask
from routes.public_state import public_state_bp

def create_app():
    app = Flask(__name__)

    # Health check
    @app.route("/")
    def health():
        return {
            "status": "ok",
            "service": "district-intelligence-backend"
        }

    app.register_blueprint(public_state_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
