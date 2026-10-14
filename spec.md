# Discount rules (v2)

1. Money is always integer cents. Never use floats for money.
2. Tier discount by subtotal:
   - below 5,000 cents: 0%
   - 5,000 to 9,999 cents: 5%
   - 10,000 cents and above: 10%  (exactly 10,000 gets 10%)
3. Loyalty members get an extra 2%, calculated AFTER the tier discount.
4. A subtotal of zero or less raises ValueError.
5. Return the final total in integer cents.
