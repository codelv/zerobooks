"""
Copyright (c) 2023, Jairus Martin.

Distributed under the terms of the AGPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from datetime import datetime
from decimal import Decimal as D

from atom.api import Int, Str, Typed
from atomdb.sql import Relation

from .base import BaseModel
from .customer import Customer
from .invoice import Invoice


class Payment(BaseModel):
    id = Int().tag(primary_key=True)
    amount = Typed(D, ())
    ref = Str().tag(length=255)

    #: Invoice paid
    invoice = Typed(Invoice).tag(nullable=False, ondelete="CASCADE")

    #: Customer
    customer = Typed(Customer).tag(nullable=False, ondelete="CASCADE")

    #: Refunds made
    refunds = Relation(lambda: Refund)

    class Meta:
        db_table = "payment"


class Refund(BaseModel):
    id = Int().tag(primary_key=True)
    amount = Typed(D, ())
    ref = Str().tag(length=255)
    payment = Typed(Payment).tag(nullable=False, ondelete="CASCADE")

    class Meta:
        db_table = "refund"
