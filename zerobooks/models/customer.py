"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from decimal import Decimal as D

from atom.api import Bool, Int, Property, Str, Typed, observe
from atomdb.sql import Relation, SQLModel
from enaml.application import Application

from .address import Address
from .base import BaseModel


class Customer(BaseModel):
    #: Customer ID
    id = Int().tag(primary_key=True)

    #: Internal
    internal = Bool()

    #: Title or Prefix
    title = Str().tag(length=10)

    #: Customer name
    first_name = Str().tag(length=50)

    #: Middle name or initial
    middle_name = Str().tag(length=50)

    #: Last name
    last_name = Str().tag(length=50)

    #: Suffix
    suffix = Str().tag(length=10)

    def _get_name(self) -> str:
        parts = [
            self.title,
            self.first_name,
            self.middle_name,
            self.last_name,
            self.suffix,
        ]
        return " ".join([p.strip() for p in parts if p])

    def _set_name(self, name: str):
        # Any matching titles sorted by length
        app = Application.instance()
        sys_config = app.sys_config
        titles = sorted(
            [x for x in sys_config.name_prefixes.keys() if x and x in name],
            key=lambda x: -len(x),
        )
        if titles:
            self.title = titles[0]
            name = self.title.join(name.split(self.title)[1:])

        suffixes = sorted(
            [x for x in sys_config.name_suffixes.keys() if x and x in name],
            key=lambda x: -len(x),
        )
        if suffixes:
            name, self.suffix = name.split(suffixes[0])

        parts = name.split(" ")
        self.first_name = parts[0]
        if len(parts) > 1:
            self.last_name = " ".join(parts[1:])
        self.name  # Trigger update

    #: Shortcut for getting and setting the name
    name = Property(_get_name, _set_name).tag(store=False)

    #: Name for display
    display_name = Str().tag(store=False)
    display_name_format = Str()

    def _default_display_name(self) -> str:
        return self.display_name_format.format(
            title=self.title,
            suffix=self.suffix,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            company=self.company,
            phone=self.phone,
            email=self.email,
        )

    @observe(
        "title",
        "suffix",
        "company",
        "phone",
        "first_name",
        "last_name",
        "middle_name",
        "display_name_format",
    )
    def _update_display_name(self, change):
        self.display_name = self._default_display_name()

    #: Company
    company = Str().tag(length=255)

    #: Email
    email = Str().tag(length=255)

    #: Phone numbers
    phone = Str().tag(length=15)
    mobile = Str().tag(length=15)
    fax = Str().tag(length=15)

    #: Addresses
    addresses = Relation(lambda: Address)
    billing_address = Typed(Address, ())
    shipping_address = Typed(Address)

    #: Website
    website = Str().tag(length=255)

    #: Notes
    notes = Str()

    #: Parent customer
    # parent = ForwardInstance(lambda: Customer)

    #: Balance
    open_balance = Typed(D, ())

    #: Total spend
    total_spend = Typed(D, ())

    class Meta:
        db_table = "customer"
