#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
""" A simple example plugin application.

This example serves to demonstrate the concepts described the accompanying
developer crash source document.

"""
import enamlx
enamlx.install()
import enaml
from atom.api import Typed
from web.components.html import Tag
from web.impl import lxml_components
from enaml.qt import QtWebEngineWidgets  # Required or it fails to import
from enaml.qt.qt_application import QtApplication, ProxyResolver
from enaml.workbench.ui.api import UIWorkbench


class ZeroApplication(QtApplication):
    #: Web component resolver
    web_resolver = Typed(ProxyResolver)
    
    def _default_web_resolver(self):
        return ProxyResolver(factories=lxml_components.FACTORIES)
    
    def resolve_proxy_class(self, declaration_class):
        """ Resolve both html and qt elements.

        """
        if issubclass(declaration_class, Tag):
            resolver = self.web_resolver
            for base in declaration_class.mro():
                name = base.__name__
                cls = resolver.resolve(name)
                if cls is not None:
                    return cls
        return super(ZeroApplication, self).resolve_proxy_class(declaration_class)
    
    def write_to_websocket(self, websocket, message):
        self.deferred_call(websocket.write_message, message)
        

def main():
    with enaml.imports():
        from .manifest import AppManifest

    workbench = UIWorkbench()
    workbench.register(AppManifest())
    workbench.run()


if __name__ == '__main__':
    main()
