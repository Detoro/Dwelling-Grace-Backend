# Thistle & Down — Backend

Flask API + Stripe Checkout. Serves the product catalog and turns a cart
into a paid order. **Every price is computed here, from raw product/option
IDs — the frontend's numbers are for display only and are never trusted.**

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env
```

## Run it

```bash
python run.py
# → http://localhost:5000
```

The Vite dev server proxies `/api/*` to this by default (see the
frontend's `vite.config.ts`), so with both running, `npm run dev` on the
frontend talks to this API out of the box.

## Stripe webhook, locally

Orders are only written to the database once Stripe confirms the payment
succeeded — via a webhook, not the checkout-creation request. To receive
that webhook locally, install the [Stripe CLI](https://stripe.com/docs/stripe-cli)
and run:

```bash
stripe listen --forward-to localhost:5000/api/checkout/webhook
```

It prints a `whsec_...` value — put that in `.env` as
`STRIPE_WEBHOOK_SECRET`. Leave `stripe listen` running while you test
checkouts.

If you check an order's receipt page before the webhook fires (e.g. you
haven't started `stripe listen` yet), `GET /api/checkout/session/<id>`
falls back to asking Stripe directly for that session, so the receipt
still renders correctly.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/products` | List products. Optional `?category=` and `?featured=true` |
| GET | `/api/products/<slug>` | Single product |
| POST | `/api/checkout/session` | Re-prices the submitted lines and creates a Stripe Checkout session |
| POST | `/api/checkout/webhook` | Stripe → us, on `checkout.session.completed` |
| GET | `/api/checkout/session/<session_id>` | Receipt for the success page |
| POST | `/api/newsletter` | Email newsletter signup |
| GET | `/api/health` | Liveness check |

## How pricing stays trustworthy

- `app/data/products.py` is the catalog — base price + variant option
  price deltas. It's the same shape the frontend uses for display, but
  this copy is authoritative.
- `app/data/designer_pricing.py` mirrors the frontend's
  `src/data/designerOptions.ts` for the Pillow/Case Designer. The two are
  hand-kept in sync; there's no shared package between the two apps.
- `app/data/catalog_pricing.py` and the `_price_line` helper in
  `app/routes/checkout.py` take a `productId` + raw selection IDs (never a
  price) and look up the real number. If a selection doesn't exist, the
  whole request is rejected with a 400 before any Stripe call is made.

## Adding a product

Add an entry to `PRODUCTS` in `app/data/products.py` — id, slug, category,
`basePrice` (cents), `variantGroups`, images, copy. No other file needs
to change; the catalog list, product page, and checkout pricing all read
from this one list.

## Database & Production notes

- **Database**: Supports PostgreSQL via `DATABASE_URL` (e.g. `postgresql://user:password@localhost:5432/dbname`) using SQLAlchemy and `psycopg`. If `DATABASE_URL` is omitted, it defaults to a local SQLite database (`sqlite:///orders.db`).
- **CORS**: locked to `FRONTEND_URL` — update it (and redeploy) when the
  frontend's real domain is live.
- **Stripe keys**: use `sk_live_...` / `pk_live_...` only once you're
  ready to take real payments, and register a production webhook
  endpoint in the Stripe Dashboard (Developers → Webhooks) instead of
  `stripe listen`.
- **WSGI server**: `gunicorn run:app` instead of `python run.py` in
  production (gunicorn is already in `requirements.txt`).
