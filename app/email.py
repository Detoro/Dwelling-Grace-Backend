import logging

from flask import current_app, render_template
from flask_mail import Message

logger = logging.getLogger(__name__)

def send_newsletter_subcription(recipient: str) -> bool:
    mail = current_app.extensions.get("mail")
    if mail is None:
        logger.warning("Mail extension is not initialized — skipping newsletter subscription email.")
        return False

    try:
        msg = Message(
            subject="Newsletter Subscription Confirmed",
            recipients=[recipient],
        )

        msg.body = (
            f"Thank you for subscribing to our newsletter!\n\n"
            f"You'll now receive updates and special offers from us.\n\n"
            f"If you did not subscribe, please ignore this email."
        )

        msg.html = render_template(
            "emails/newsletter_subscription.html",
            recipient=recipient,
        )

        mail.send(msg)
        logger.info("Newsletter subscription email sent to %s", recipient)
        return True

    except Exception:
        logger.exception("Failed to send newsletter subscription email to %s", recipient)
        return False

def send_order_confirmation(recipient: str, order_id: str, total: int, lines: list[dict]) -> bool:
    mail = current_app.extensions.get("mail")
    if mail is None:
        logger.warning("Mail extension is not initialized — skipping order confirmation email.")
        return False

    try:
        msg = Message(
            subject=f"Order Confirmed — {order_id}",
            recipients=[recipient],
        )

        item_lines = "\n".join(
            f"  • {line['name']} x{line['quantity']}  —  ${line['unitPrice'] / 100:.2f} each"
            for line in lines
        )
        msg.body = (
            f"Thank you for your order!\n\n"
            f"Order ID: {order_id}\n\n"
            f"Items:\n{item_lines}\n\n"
            f"Total: ${total / 100:.2f}\n\n"
            f"We'll send you another email when your order ships."
        )

        msg.html = render_template(
            "emails/order_confirmation.html",
            order_id=order_id,
            total=total,
            lines=lines,
        )

        mail.send(msg)
        logger.info("Order confirmation email sent to %s for order %s", recipient, order_id)
        return True

    except Exception:
        logger.exception("Failed to send order confirmation email to %s for order %s", recipient, order_id)
        return False