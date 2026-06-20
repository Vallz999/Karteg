from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# import routes
from routes.auth_routes import auth_bp
from routes.kategori_routes import kategori_bp
from routes.lauk_routes import lauk_bp
from routes.transaksi_routes import transaksi_bp
from routes.dashboard_routes import dashboard_bp
from routes.riwayat_routes import riwayat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(
        app,
        supports_credentials=True,
            origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ]
    )

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(kategori_bp, url_prefix="/api/kategori")
    app.register_blueprint(lauk_bp, url_prefix="/api/lauk")
    app.register_blueprint(transaksi_bp, url_prefix="/api/transaksi")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(riwayat_bp, url_prefix="/api/riwayat")

    @app.route("/")
    def home():
        return jsonify({
            "status": "success",
            "message": "KarTeg Backend Running"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Endpoint not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )