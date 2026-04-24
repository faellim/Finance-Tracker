from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP


CENT_FACTOR = Decimal("100")


def decimal_to_cents(amount: Decimal) -> int:
    normalized = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(normalized * CENT_FACTOR)


def cents_to_decimal(cents: int) -> Decimal:
    return (Decimal(cents) / CENT_FACTOR).quantize(Decimal("0.01"))
