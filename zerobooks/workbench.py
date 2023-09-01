"""
Copyright (c) 2023, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from typing import Optional

from atom.api import Str
from enaml.qt.QtWidgets import QMessageBox
from enaml.workbench.ui.api import UIWorkbench

from .utils import log


class ZeroWorkbench(UIWorkbench):
    #: For error messages
    app_name = Str("ZeroBooks")

    @property
    def application(self):
        ui = self.get_plugin("enaml.workbench.ui")
        return ui._application

    @property
    def window(self):
        """Return the main UI window or a dialog if it wasn't made yet
        (during loading)

        """
        ui = self.get_plugin("enaml.workbench.ui")
        return ui.window.proxy.widget

    def message_warning(self, title, message, *args, **kwargs):
        """Shortcut to display a warning popup dialog."""
        log.warning(message)
        return QMessageBox.warning(
            self.window, f"{self.app_name} - {title}", message, *args, **kwargs
        )

    def message_question(
        self, title: str, message: str, *args, **kwargs
    ) -> Optional[bool]:
        """Shortcut to display a question popup dialog."""
        log.info(message)
        r = QMessageBox.question(
            self.window,
            f"{self.app_name} - {title}",
            message,
            *args,
            **kwargs,
        )
        if r == QMessageBox.Yes:
            return True
        elif r == QMessageBox.No:
            return False
        return None
