from uuid import uuid4
from atom.api import (
    Atom, Property, Instance, Enum, Unicode, List, Dict, ForwardInstance, Float,
    observe
)
from .config import System, Model


class Address(Model):
    #: Street
    street = Unicode()
    
    #: City
    city = Unicode()
    
    #: States
    state = Enum(*System.instance().states)
    
    #: Zipcodes
    zipcode = Unicode()
    
    #: Countries
    country = Enum('US')
    
    
class Customer(Model):
    #: Customer ID
    uuid = Unicode()
    
    def _default_uuid(self):
        return str(uuid4())
    
    #: Name
    #: Title or Prefix
    title = Enum('', *System.instance().name_prefixes.keys())
    
    #: Customer name
    first_name = Unicode()
    
    #: Middle name or initial
    middle_name = Unicode()
    
    #: Last name
    last_name = Unicode()
    
    #: Suffix
    suffix = Enum('', *System.instance().name_suffixes.keys())
    
    
    def _get_name(self):
        parts = [self.title, self.first_name, self.middle_name, 
                 self.last_name, self.suffix]
        return " ".join([p.strip() for p in parts if p])
    
    def _set_name(self, name):
        # Any matching titles sorted by length
        titles = sorted([x for x in Customer.title.items if x and x in name],
                        key=lambda x: -len(x))
        if titles:
            self.title = titles[0]
            name = self.title.join(name.split(self.title)[1:])
        
        suffixes = sorted([x for x in Customer.suffix.items if x and x in name],
                           key=lambda x: -len(x))
        if suffixes:
            name, self.suffix = name.split(suffixes[0])
        
        parts = name.split(" ")
        self.first_name = parts[0]
        if len(parts) > 1:
            self.last_name = " ".join(parts[1:])
        self.name # Trigger update
    
    #: Shortcut for getting and setting the name
    name = Property(_get_name, _set_name)
    
    #: Name for display 
    display_name = Unicode()
    display_name_format = Enum(*System.instance().display_name_formats)
    
    def _default_display_name(self):
        return self.display_name_format.format(
            title=self.title,
            suffix=self.suffix,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
        )
    
    @observe('title', 'suffix', 'first_name', 'last_name', 'middle_name',
             'display_name_format')
    def _update_display_name(self, change):
        self.display_name = self._default_display_name()
    
    #: Company
    company = Unicode()
        
    #: Email
    email = Unicode()
    
    #: Phone numbers
    phone = Unicode()
    mobile = Unicode()
    fax = Unicode()
    
    #: Addresses
    addresses = List(Address)
    billing_address = Instance(Address, ())
    shipping_address = Instance(Address)

    #: Website
    website = Unicode()
    
    #: Notes
    notes = Unicode()
    
    #: Parent customer
    parent = ForwardInstance(lambda: Customer)
    
    #: Balance
    open_balance = Float()
