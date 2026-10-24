from django.conf import settings
from stripe import StripeClient

def get_stripe_client():
    return StripeClient(settings.STRIPE_SECRET_CODE)

def create_stripe_product(course):
    client = get_stripe_client()

    product = client.v1.products.create({
        "name": course.title,
        "description": course.description or "",
    })

    return product

def create_stripe_price(product_id, amount_cents):
    client = get_stripe_client()

    price = client.v1.prices.create({
        "product": product_id,
        "unit_amount":  amount_cents,
        "currency": "usd"
    })

    return price

def create_stripe_session(price_id):
    client = get_stripe_client()

    session = client.v1.checkout.sessions.create({
        "mode": "payment",
        "line_items":[
            {"price": price_id, "quantity": 1},
        ],
        "success_url": "http://127.0.0.1:8000/api/docs/",
        "cancel_url": "http://127.0.0.1:8000/api/docs/"
    })
    return session

def create_stripe_checkout(course, amount):
    product = create_stripe_product(course)

    amount_cents = int(amount * 100)
    price = create_stripe_price(product.id, amount_cents)

    session = create_stripe_session(price.id)

    return {
        "stripe_product_id": product.id,
        "stripe_price_id": price.id,
        "stripe_session_id" : session.id,
        "payment_url": session.url,
    }