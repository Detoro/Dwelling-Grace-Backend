import logging

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config, validate_config
from app.orders import init_db


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}})

    db_uri = app.config.get("DATABASE_URL") or app.config.get("DATABASE_PATH", "orders.db")
    init_db(db_uri)

    for warning in validate_config(Config):
        app.logger.warning(warning)
    logging.basicConfig(level=logging.INFO)

    from app.routes.checkout import bp as checkout_bp
    from app.routes.newsletter import bp as newsletter_bp
    from app.routes.products import bp as products_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(newsletter_bp)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": str(err.description) if hasattr(err, "description") else "Not found"}), 404

    return app
