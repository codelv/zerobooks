import pickle

from atom.api import Unicode, Subclass, Bytes, ContainerList, Instance

from enaml.widgets.api import Container, DockArea,  DockItem
from enaml.workbench.api import Plugin, PluginManifest
from enaml.workbench.ui.api import Workspace
from enaml.layout.api import InsertItem, InsertTab


import enaml
with enaml.imports():
    from .views.dock import DockManifest, DockView

from zero.models.customer import Customer, Address
from zero.models.invoice import Invoice, InvoiceItem


class CorePlugin(Plugin):
    #: Pickled dock state
    state = Bytes()
    
    #: Company info
    company = Instance(Customer, ())
    
    #: Customers
    customers = ContainerList(Customer)
    
    #: Invoices
    invoices = ContainerList(Invoice)
    
    #: Dock items added
    items = ContainerList(DockItem)
    
    #: Dock area
    area = Instance(DockArea)
    
    def start(self):
        # Start the first workspace
        ui = self.workbench.get_plugin("enaml.workbench.ui")
        ui.select_workspace("zero.core.default_view")
        self.load_data()
        
    def insert_item(self, item, **kwargs):
        if not isinstance(item, DockItem):
            raise TypeError("Invalid item: {}".format(item))
        op = InsertTab(item=item.name, **kwargs)
        self.area.update_layout(op)
        
    def load_data(self):
        self._load_test_data()
        
    def _load_test_data(self):
        import arrow
        import random
        from faker import Faker
        faker = Faker()
        
        customers = [Customer()
                     for i in range(faker.random_int(max=1000))]
        
        for c in [self.company]+customers:
            profile = faker.profile()
            c.company = profile['company']
            c.name = profile['name']
            c.website = ", ".join(profile['website'])
            c.email = profile['mail']
            c.phone = faker.phone_number()
            
            c.billing_address.street, addr = profile['address'].split("\n")
            addr = addr.split(",")
            if len(addr) > 1:
                c.billing_address.city, *addr = addr
            addr = ",".join(addr)
            c.billing_address.zipcode = addr.split()[-1]
            
            if faker.random_int(max=10) > 8:
                c.shipping_address = Address()
                c.shipping_address.street, addr = faker.address().split("\n")
                addr = addr.split(",")
                if len(addr) > 1:
                    c.shipping_address.city, *addr = addr
                addr = ",".join(addr)
                c.shipping_address.zipcode = addr.split()[-1]
        
        self.customers = customers
        
        invoices = []
        for i in range(faker.random_int(max=1000)):
            items = [InvoiceItem(
                    name=faker.bs(),
                    rate=int(abs(random.gauss(25, 100))),
                    quantity=faker.random_int(max=100),
                ) for j in range(faker.random_int(max=10))]
            invoices.append(Invoice(
                owner=self.company,
                customer=faker.random_element(customers),
                date=arrow.get(faker.date()),
                items=items,
            ))
        self.invoices = invoices
            
        


class DefaultWorkspace(Workspace):
    """ A custom Workspace class for the crash course example.

    """
    #: The enamldef'd Container to create when the workbench is started.
    content_def = Subclass(Container)

    #: The enamldef'd PluginManifest to register on start.
    manifest_def = Subclass(PluginManifest)

    #: Storage for the plugin manifest's id.
    _manifest_id = Unicode()
    
    def start(self):
        """ Start the workspace instance.

        This method will create the container content and register the
        provided plugin with the workbench.

        """
        self.content = self.content_def()
        self.load_area()
        manifest = self.manifest_def()
        self._manifest_id = manifest.id
        self.workbench.register(manifest)

    def stop(self):
        """ Stop the workspace instance.

        This method will unregister the workspace's plugin that was
        registered on start.

        """
        self.save_area()
        self.workbench.unregister(self._manifest_id)

    def save_area(self):
        """ Save the dock area for the workspace.

        """
        plugin = self.workbench.get_plugin('zero.core')
        area = self.content.find('the_dock_area')
        plugin.state = pickle.dumps(area, -1)
        del plugin.area

    def load_area(self):
        """ Load the dock area into the workspace content.

        """
        plugin = self.workbench.get_plugin('zero.core')
        if plugin.state:
            area = pickle.loads(plugin.state)
        else:
            area = DockView(workbench=self.workbench)
        area.set_parent(self.content)
        plugin.area = area
