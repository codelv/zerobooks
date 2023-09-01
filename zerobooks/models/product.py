"""
Copyright (c) 2023, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from decimal import Decimal as D

from atom.api import Bool, Int, Str, Typed

from .base import BaseModel


class Product(BaseModel):
    id = Int().tag(primary_key=True)
    name = Str().tag(length=255)
    description = Str()
    price = Typed(D, ())
    taxable = Bool()

    class Meta:
        db_table = "product"
