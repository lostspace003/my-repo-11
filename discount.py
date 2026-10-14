def final_total(subtotal_cents, loyalty=False):
    """Return the total after discounts."""
    rate = 0.0
    if subtotal_cents > 10000:
        rate = 0.10
    elif subtotal_cents >= 5000:
        rate = 0.05
    if loyalty:
        rate += 0.02
    return round(subtotal_cents * (1 - rate))
