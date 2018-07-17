import enaml
import arrow
from uuid import uuid4
from atom.api import (
    Property, Instance, Enum, Unicode, List, Dict, ForwardInstance, Float,
    Int, ContainerList, observe
)
from .config import System, Model
from .customer import Customer
from web.components.api import Html


class InvoiceItem(Model):
    #: Product or service
    name = Unicode()
    
    #: Extra information
    description = Unicode()
    
    #: Quantity
    quantity = Float(1)
    
    #: Rate
    rate = Float()
    
    #: Line amount
    amount = Float()
    
    def _default_amount(self):
        return self.quantity * self.rate
    
    @observe('rate', 'quantity')
    def _update_amount(self, change):
        self.amount = self._default_amount()
    

class Invoice(Model):
    #: Invoice ID
    uuid = Unicode()
    
    #: Invoice number
    __counter__ = 10000
    number = Int()
    
    def _default_number(self):
        n = Invoice.__counter__
        Invoice.__counter__ +=1
        return n
    
    def _default_uuid(self):
        return str(uuid4())
    
    #: Invoice date
    date = Instance(arrow.Arrow, factory=arrow.now)
    
    #: Due date
    due_date = Instance(arrow.Arrow)
    
    #: Due date
    terms = Enum(*System.instance().invoice_terms.keys())
    
    def _default_terms(self):
        return 'Net 30'
    
    def _default_due_date(self):
        # TODO: Handle all the terms
        t = self.terms
        days = 30
        if 'Net ' in t:
            days = int(t.split()[-1])
        elif 'EOM':
            d = self.date.datetime
            eom = self.date.shift(months=1, days=-(d.day-1))
            dt = eom - self.date
            days = dt.days
        return self.date.shift(days=days)
    
    @observe('date', 'terms')
    def _update_due_date(self, change):
        self.due_date = self._default_due_date()
    
    #: Invoicer
    owner = Instance(Customer)
    
    #: Invoicer
    customer = Instance(Customer)
    
    #: Notes
    notes = Unicode()
    
    #: Items
    items = ContainerList(InvoiceItem)
    
    #: Balance
    total_amount = Float()
    
    #: Template
    view = Instance(Html)
    
    def _default_total_amount(self):
        return sum([i.amount for i in self.items])
    
    @observe('items')
    def _update_totals(self, change):
        # TODO: Handle removed
        for item in self.items:
            item.unobserve('amount', self._update_totals)
            item.observe('amount', self._update_totals)
            
        self.total_amount = self._default_total_amount()
        
    def _default_view(self):
        with enaml.imports():
            from zero.templates.invoice import InvoiceTemplate
        return InvoiceTemplate(invoice=self)
        
