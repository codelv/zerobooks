"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the AGPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Jul 17, 2018
"""
import logging
import os
import sys
from typing import Optional

from enaml.core.declarative import d_func
from enaml.icon import Icon, IconImage
from enaml.image import Image
from enaml.widgets.api import DockArea as CoreDockArea
from enaml.widgets.api import DockItem as CoreDockItem

# -----------------------------------------------------------------------------
# Logger
# -----------------------------------------------------------------------------
log = logging.getLogger("zerobooks")
CONFIG_DIR = os.path.expanduser("~/.config/zerobooks/")
DB_FILE = os.path.join(CONFIG_DIR, "zerobooks.db")


# -----------------------------------------------------------------------------
# Icon and Image helpers
# -----------------------------------------------------------------------------
#: Cache for icons
_IMAGE_CACHE = {}


def clip(s, n=1000):
    """Shorten the name of a large value when logging"""
    v = str(s)
    if len(v) > n:
        v = v[:n] + "..."
    return v


def icon_path(name: str) -> str:
    """Load an icon from the res/icons folder using the name
    without the .png

    """
    path = os.path.dirname(__file__)
    return os.path.join(path, "assets", "icons", "%s.png" % name)


def load_image(name: str) -> Image:
    """Get and cache an enaml Image for the given icon name."""
    path = icon_path(name)
    global _IMAGE_CACHE
    if path not in _IMAGE_CACHE:
        with open(path, "rb") as f:
            data = f.read()
        _IMAGE_CACHE[path] = Image(data=data)
    return _IMAGE_CACHE[path]


def load_icon(name: str) -> Icon:
    img = load_image(name)
    icg = IconImage(image=img)
    return Icon(images=[icg])


def menu_icon(name: str) -> Optional[str]:
    """Icons don't look good on Linux/osx menu's"""
    if sys.platform == "win32":
        return load_icon(name)
    return None


def safe_search(scope: dict, query: str) -> bool:
    """Perform a safe search expression evaluation by parsing the query
    ast and computing the value from the scope.

    Returns
    -------
    matched: Bool or None for error
        Whether the item in the scope matches the query


    """
    # TODO: Do not use eval but instead parse the ast
    return bool(eval(query, {}, scope))


class DockItem(CoreDockItem):
    """A custom pickable dock item class."""

    def __getstate__(self):
        """Get the pickle state for the dock item.

        This method saves the necessary state for the dock items used
        in this example. Different applications will have different
        state saving requirements.

        The default __setstate__ method provided on the Atom base class
        provides sufficient unpickling behavior.

        """
        return self.save_state()

    @d_func
    def save_state(self) -> dict:
        return {
            "name": self.name,
            "title": self.title,
        }


class DockArea(CoreDockArea):
    """A custom pickable dock area class."""

    def get_save_items(self):
        """Get the list of dock items to save with this dock area."""
        return [c for c in self.children if isinstance(c, DockItem)]

    def __getstate__(self):
        """Get the pickle state for the dock area.

        This method saves the necessary state for the dock area used
        in this example. Different applications will have different
        state saving requirements.

        """
        state = {
            "name": self.name,
            "layout": self.save_layout(),
            "items": self.get_save_items(),
        }
        return state

    def __setstate__(self, state):
        """Restore the state of the dock area."""
        self.name = state["name"]
        self.layout = state["layout"]
        self.insert_children(None, state["items"])
