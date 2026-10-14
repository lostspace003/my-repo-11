from billing import add_tax


def order_total(items):
    """Return the order total in cents. items is a list of (price_cents, qty)."""
    subtotal = sum(price * qty for price, qty in items)
    return add_tax(subtotal)


# TODO(SHOP-41): support gift cards
def confirm(order_id):
    return f"Order {order_id} Recieved"
