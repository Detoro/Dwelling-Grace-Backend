import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    session_id = Column(String(255), primary_key=True)
    order_id = Column(String(64), nullable=False)
    email = Column(String(255), nullable=False, default="")
    total = Column(Integer, nullable=False)
    lines_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "orderId": self.order_id,
            "email": self.email,
            "total": self.total,
            "lines": json.loads(self.lines_json),
        }


class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Product(Base):
    __tablename__ = "products"

    id = Column(String(64), primary_key=True)
    slug = Column(String(128), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(64), nullable=False, index=True)
    base_price = Column(Integer, nullable=False)
    images_json = Column(Text, nullable=False, default="[]")
    short_description = Column(Text, nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    care_notes = Column(Text, nullable=False, default="")
    shipping_notes = Column(Text, nullable=False, default="")
    featured = Column(Boolean, default=False, index=True)
    variant_groups_json = Column(Text, nullable=False, default="[]")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "category": self.category,
            "basePrice": self.base_price,
            "images": json.loads(self.images_json),
            "shortDescription": self.short_description,
            "description": self.description,
            "careNotes": self.care_notes,
            "shippingNotes": self.shipping_notes,
            "featured": self.featured,
            "variantGroups": json.loads(self.variant_groups_json),
        }


class DesignerOption(Base):
    __tablename__ = "designer_options"

    id = Column(String(64), primary_key=True)
    group_type = Column(String(64), nullable=False, index=True)
    label = Column(String(128), nullable=False)
    price_delta = Column(Integer, nullable=False, default=0)
    swatch_hex = Column(String(32), nullable=True)
    weave = Column(String(32), nullable=True)
    display_order = Column(Integer, nullable=False, default=0)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "label": self.label,
            "priceDelta": self.price_delta,
        }
        if self.swatch_hex:
            data["swatchHex"] = self.swatch_hex
        if self.weave:
            data["weave"] = self.weave
        return data


_engines: Dict[str, Any] = {}
_session_factories: Dict[str, Any] = {}


def _normalize_uri(db_uri_or_path: str) -> str:
    if not db_uri_or_path:
        return "sqlite:///orders.db"
    if "://" not in db_uri_or_path:
        return f"sqlite:///{db_uri_or_path}"
    if db_uri_or_path.startswith("postgres://"):
        return db_uri_or_path.replace("postgres://", "postgresql+psycopg://", 1)
    if db_uri_or_path.startswith("postgresql://") and not db_uri_or_path.startswith("postgresql+"):
        return db_uri_or_path.replace("postgresql://", "postgresql+psycopg://", 1)
    return db_uri_or_path


def get_engine(db_uri: str):
    uri = _normalize_uri(db_uri)
    if uri not in _engines:
        if uri.startswith("sqlite"):
            _engines[uri] = create_engine(uri, connect_args={"check_same_thread": False})
        else:
            _engines[uri] = create_engine(uri, pool_pre_ping=True)
        _session_factories[uri] = sessionmaker(bind=_engines[uri], expire_on_commit=False)
    return _engines[uri]


def get_session(db_uri: str):
    uri = _normalize_uri(db_uri)
    if uri not in _session_factories:
        get_engine(uri)
    return _session_factories[uri]()


def init_db(db_uri: str) -> None:
    """Initializes schema, tables, and automatically seeds initial data if empty."""
    try:
        engine = get_engine(db_uri)
        Base.metadata.create_all(bind=engine)
        from app.seed import seed_database
        seed_database(db_uri, force=False)
    except Exception as exc:
        logger.warning(f"Database initialization warning (will retry on demand): {exc}")

def get_all_products(db_uri: str, category: Optional[str] = None, featured: Optional[bool] = None) -> List[Dict[str, Any]]:
    session = get_session(db_uri)
    try:
        stmt = select(Product)
        if category:
            stmt = stmt.where(Product.category == category)
        if featured is not None:
            stmt = stmt.where(Product.featured == featured)
        stmt = stmt.order_by(Product.created_at.asc())
        products = session.execute(stmt).scalars().all()
        return [p.to_dict() for p in products]
    finally:
        session.close()


def get_product_by_slug(db_uri: str, slug: str) -> Optional[Dict[str, Any]]:
    session = get_session(db_uri)
    try:
        stmt = select(Product).where(Product.slug == slug)
        product = session.execute(stmt).scalar_one_or_none()
        return product.to_dict() if product is not None else None
    finally:
        session.close()


def get_product_by_id(db_uri: str, product_id: str) -> Optional[Dict[str, Any]]:
    session = get_session(db_uri)
    try:
        product = session.get(Product, product_id)
        return product.to_dict() if product is not None else None
    finally:
        session.close()


def get_designer_options(db_uri: str) -> Dict[str, Any]:
    session = get_session(db_uri)
    try:
        stmt = select(DesignerOption).order_by(DesignerOption.display_order.asc())
        options = session.execute(stmt).scalars().all()

        fabrics = []
        sizes = []
        piping = []
        closures = []
        monogram_textures = []
        monogram_fonts = []
        case_sizes = []

        for opt in options:
            d = opt.to_dict()
            if opt.group_type == "fabric":
                fabrics.append(d)
            elif opt.group_type == "size":
                sizes.append(d)
            elif opt.group_type == "piping":
                piping.append(d)
            elif opt.group_type == "closure":
                closures.append(d)
            elif opt.group_type == "monogram_texture":
                monogram_textures.append(d)
            elif opt.group_type == "monogram_font":
                monogram_fonts.append(d)
            elif opt.group_type == "case_size":
                case_sizes.append(d)

        return {
            "fabrics": fabrics,
            "sizes": sizes,
            "piping": piping,
            "closures": closures,
            "monogramTextures": monogram_textures,
            "monogramFonts": monogram_fonts,
            "caseSizes": case_sizes,
            "pillowBasePrice": 1899,
            "caseBasePrice": 5800,
        }
    finally:
        session.close()


def get_designer_option_by_id(db_uri: str, option_id: str) -> Optional[Dict[str, Any]]:
    session = get_session(db_uri)
    try:
        opt = session.get(DesignerOption, option_id)
        return opt.to_dict() if opt is not None else None
    finally:
        session.close()

def save_order(
    db_uri: str,
    session_id: str,
    order_id: str,
    email: str,
    total: int,
    lines: List[dict],
) -> None:
    session = get_session(db_uri)
    try:
        order = session.get(Order, session_id)
        if order is None:
            order = Order(
                session_id=session_id,
                order_id=order_id,
                email=email,
                total=total,
                lines_json=json.dumps(lines),
            )
            session.add(order)
        else:
            order.order_id = order_id
            order.email = email
            order.total = total
            order.lines_json = json.dumps(lines)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_order_by_session_id(db_uri: str, session_id: str) -> Optional[dict]:
    session = get_session(db_uri)
    try:
        order = session.get(Order, session_id)
        if order is None:
            return None
        return order.to_dict()
    finally:
        session.close()

def subscribe_newsletter(db_uri: str, email: str) -> bool:
    cleaned_email = email.strip().lower()
    if not cleaned_email or "@" not in cleaned_email:
        raise ValueError("Invalid email address")

    session = get_session(db_uri)
    try:
        stmt = select(NewsletterSubscriber).where(NewsletterSubscriber.email == cleaned_email)
        existing = session.execute(stmt).scalar_one_or_none()
        if existing is not None:
            return True
        subscriber = NewsletterSubscriber(email=cleaned_email)
        session.add(subscriber)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
