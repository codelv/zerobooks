"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
import os
import pickle
from typing import Optional

import enaml
from atom.api import Bytes, ContainerList, Instance, Str, Subclass
from enaml.application import deferred_call
from enaml.layout.api import (
    AreaLayout,
    DockBarLayout,
    HSplitLayout,
    InsertTab,
    TabLayout,
    VSplitLayout,
)
from enaml.widgets.api import Container, DockArea, DockItem
from enaml.workbench.api import Plugin, PluginManifest
from enaml.workbench.ui.api import Workspace

with enaml.imports():
    from .views.dock import (
        DockView,
        CompanyDockItem,
        CustomersDockItem,
        InvoicesDockItem,
        ProductsDockItem,
    )
    from enaml.stdlib.dock_area_styles import available_styles

from zerobooks.models.api import Address, Customer, Invoice, Product
from zerobooks.utils import CONFIG_DIR, log

# Workbench layout is saved here
STATE_FILE = os.path.join(CONFIG_DIR, "core.pk")


class CorePlugin(Plugin):
    #: Pickled dock state
    state = Bytes()

    #: Company info
    company = Instance(Customer, ())

    addresses = ContainerList(Address)

    #: Customers
    customers = ContainerList(Customer)

    #: Invoices
    invoices = ContainerList(Invoice)

    #: Products
    products = ContainerList(Product)

    #: Dock items added
    items = ContainerList(DockItem)

    #: Dock area
    area = Instance(DockArea)

    #: Path last saved
    last_save_dir = Str(".")

    def start(self):
        # Start the first workspace
        ui = self.workbench.get_plugin("enaml.workbench.ui")
        ui.select_workspace("zerobooks.core.default_view")
        deferred_call(self.load_data())

    def insert_item(self, item, **kwargs):
        if not isinstance(item, DockItem):
            raise TypeError("Invalid item: {}".format(item))
        op = InsertTab(item=item.name, **kwargs)
        self.area.update_layout(op)

    def _default_state(self):
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "rb") as f:
                    return pickle.load(f)
            else:
                log.debug("Core plugin state does not exist")
        except Exception as e:
            log.exception(e)
        return b""

    def _observe_state(self, change):
        if change["type"] == "update" and len(change["value"]) > 4:
            try:
                state_dir = os.path.dirname(STATE_FILE)
                if not os.path.exists(state_dir):
                    os.makedirs(state_dir)
                with open(STATE_FILE, "wb") as f:
                    pickle.dump(change["value"], f)
                log.debug("Wrote core plugin state")
            except Exception as e:
                log.exception(e)

    async def load_data(self):
        # self._load_test_data()
        self.addresses = await Address.objects.all()
        self.products = await Product.objects.all()
        self.company, _ = await Customer.objects.get_or_create(internal=True)
        self.customers = await Customer.objects.filter(internal=False)
        self.invoices = await Invoice.objects.all()

    def create_area(self, workbench):
        area = DockView(workbench=workbench)
        CompanyDockItem(area)
        CustomersDockItem(area)
        InvoicesDockItem(area)
        ProductsDockItem(area)

        area.layout = AreaLayout(
            HSplitLayout(
                VSplitLayout("customer-list", "product-list"),
                TabLayout("invoice-list", "company-view"),
            ),
        )
        return area

    def save_state(self):
        # Triggers save in _observe_state
        self.state = pickle.dumps({
            'area': self.area,
            'last_save_dir': self.last_save_dir,
        })
        del self.area

    def restore_state(self):
        if data := self.state:
            try:
                state = pickle.loads(data)
                self.area = state['area']
                self.last_save_dir = state['last_save_dir']
            except Exception as e:
                log.exception(e)


class DefaultWorkspace(Workspace):
    """A custom Workspace class for the crash course example."""

    #: The enamldef'd Container to create when the workbench is started.
    content_def = Subclass(Container)

    #: The enamldef'd PluginManifest to register on start.
    manifest_def = Subclass(PluginManifest)

    #: Storage for the plugin manifest's id.
    _manifest_id = Str()

    plugin_id = Str()

    def start(self):
        """Start the workspace instance.

        This method will create the container content and register the
        provided plugin with the workbench.

        """
        self.content = self.content_def()
        self.load_area()
        manifest = self.manifest_def()
        self._manifest_id = manifest.id
        self.workbench.register(manifest)

    def stop(self):
        """Stop the workspace instance.

        This method will unregister the workspace's plugin that was
        registered on start.

        """
        self.save_area()
        self.workbench.unregister(self._manifest_id)

    def save_area(self):
        """Save the dock area for the workspace."""
        plugin = self.workbench.get_plugin(self.plugin_id)
        if area := self.content.find("dock-area"):
            log.debug(f"Saving area {self.plugin_id}")
            plugin.area = area
            plugin.save_state()

    def reset_area(self):
        log.debug(f"Reset area {self.plugin_id}")
        workbench = self.workbench
        plugin = workbench.get_plugin(self.plugin_id)
        plugin.state = b""
        del plugin.area
        workbench.unregister(self._manifest_id)
        self.start()

    def load_area(self):
        """Load the dock area into the workspace content."""
        log.debug(f"Loading area {self.plugin_id}")
        workbench = self.workbench
        plugin = workbench.get_plugin(self.plugin_id)
        plugin.restore_state()
        if area := plugin.area:
            area.workbench = workbench
        else:
            area = plugin.create_area(workbench)
        area.set_parent(self.content)
        plugin.area = area
