TAX_RATE = 0.18


def add_tax(amount_cents):
    """Add 18% tax. Amounts are in cents."""
    return round(amount_cents * (1 + TAX_RATE))


def discount(amount_cents, percent):
    # TODO: check that percent is between 0 and 100
    return amount_cents - amount_cents * percent // 100
