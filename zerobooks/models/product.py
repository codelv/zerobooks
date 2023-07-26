"""
Copyright (c) 2023, Jairus Martin.

Distributed under the terms of the AGPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from datetime import datetime
from decimal import Decimal as D
from uuid import uuid4

from atom.api import Bool, Int, Str, Typed
from atomdb.sql import SQLModel


class Product(SQLModel):
    id = Int().tag(primary_key=True)
    uuid = Str(factory=lambda: str(uuid4().hex)).tag(length=36, unique=True)

    name = Str().tag(length=255)
    price = Typed(D, ())
    taxable = Bool()

    #: Dates
    created = Typed(datetime, factory=datetime.now)
    updated = Typed(datetime, factory=datetime.now)

    class Meta:
        db_table = "product"
