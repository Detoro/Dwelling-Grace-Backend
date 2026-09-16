import os
from dotenv import load_dotenv

load_dotenv()


def _get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        db_path = os.environ.get("DATABASE_PATH", "orders.db")
        return f"sqlite:///{db_path}"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and not url.startswith("postgresql+"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Config:
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
    DATABASE_URL = _get_database_url()
    DATABASE_PATH = os.environ.get("DATABASE_PATH", "orders.db")
    SECRET_KEY = os.environ.get("DATABASE_KEY", "dev")

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "1", "t"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "")

def validate_config(config: Config) -> list[str]:
    warnings = []
    if not config.STRIPE_SECRET_KEY:
        warnings.append("STRIPE_SECRET_KEY is not set — checkout will fail until it is.")
    if not config.STRIPE_WEBHOOK_SECRET:
        warnings.append("STRIPE_WEBHOOK_SECRET is not set — orders won't be recorded after payment.")
    if not config.MAIL_USERNAME or not config.MAIL_DEFAULT_SENDER:
        warnings.append("MAIL_USERNAME or MAIL_DEFAULT_SENDER is not set — transactional emails will not be sent.")
    return warnings
