"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the AGPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from datetime import datetime, timedelta
from decimal import Decimal as D
from uuid import uuid4

import enaml
from atom.api import ContainerList, Enum, Instance, Int, Str, Typed, observe
from atomdb.sql import JSONModel, SQLModel
from web.components.api import Html

from .customer import Customer


class InvoiceItem(JSONModel):
    #: ID
    id = Int().tag(primary_key=True)

    #: Product or service
    name = Str()

    #: Extra information
    description = Str()

    #: Quantity
    quantity = Typed(D, (1,))

    #: Rate
    rate = Typed(D, ())

    #: Line amount
    amount = Typed(D, ())

    def _default_amount(self) -> D:
        return self.quantity * self.rate

    @observe("rate", "quantity")
    def _update_amount(self, change):
        self.amount = self._default_amount()


class Invoice(SQLModel):
    #: Address ID
    id = Int().tag(primary_key=True)

    #: UUID
    uuid = Str(factory=lambda: str(uuid4().hex)).tag(length=36, unique=True)

    #: Invoice number
    __counter__ = 10000
    number = Int()

    def _default_number(self):
        n = Invoice.__counter__
        Invoice.__counter__ += 1
        return n

    created = Typed(datetime, factory=datetime.now)
    updated = Typed(datetime, factory=datetime.now)

    #: Invoice date
    date = Typed(datetime, factory=datetime.now)

    #: Due date
    due_date = Typed(datetime, factory=datetime.now)

    #: Due date
    terms = Str().tag(length=50)  # Enum(*System.instance().invoice_terms.keys())

    def _default_terms(self):
        return "Net 30"

    def _default_due_date(self):
        # TODO: Handle all the terms
        t = self.terms
        days = 30
        if "Net " in t:
            days = int(t.split()[-1])
        elif "EOM":
            d = self.date.datetime
            eom = self.date.shift(months=1, days=-(d.day - 1))
            dt = eom - self.date
            days = dt.days
        return self.date + timedelta(days=days)

    @observe("date", "terms")
    def _update_due_date(self, change):
        self.due_date = self._default_due_date()

    #: Invoicer
    owner = Typed(Customer)

    #: Invoicer
    customer = Typed(Customer)

    #: Notes
    notes = Str()

    #: Project
    project = Str().tag(length=255)

    #: Items
    items = ContainerList(InvoiceItem)

    #: Balance
    subtotal = Typed(D, ())

    #: Balance
    total_adjustments = Typed(D, ())

    #: Balance
    total_tax = Typed(D, ())

    #: Balance
    total_amount = Typed(D, ())

    #: Status
    status = Enum("pending", "open", "paid", "void").tag(length=10)

    #: Template
    view = Instance(Html).tag(store=False)

    def _default_subtotal(self) -> D:
        subtotal = D()
        for i in self.items:
            subtotal += i.amount
        return subtotal

    def _default_total_amount(self):
        return self.subtotal + self.total_tax + self.total_adjustments

    @observe("items")
    def _update_totals(self, change):
        # TODO: Handle removed
        for item in self.items:
            item.unobserve("amount", self._update_totals)
            item.observe("amount", self._update_totals)

        self.subtotal = self._default_subtotal()
        self.total_amount = self._default_total_amount()

    def _default_view(self) -> Html:
        with enaml.imports():
            from zerobooks.templates.invoice import InvoiceTemplate
        return InvoiceTemplate(invoice=self)

    def generate_filename(self) -> str:
        if customer := self.customer:
            return f"invoice-{self.number}-{customer.display_name}.pdf"
        return f"invoice-{self.number}.pdf"

    class Meta:
        db_table = "invoice"
