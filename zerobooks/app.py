"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
import asyncio
import logging
import os
import warnings
from inspect import iscoroutine
from queue import Empty, Queue
from typing import Optional

import enaml
import enamlx
from aiosqlite.sa import create_engine
from asyncqtpy import QEventLoopPolicy
from atom.api import Bool, ForwardTyped, Typed
from atomdb.sql import SQLModelManager
from enaml.qt.qt_application import ProxyResolver, QtApplication
from web.components.html import Tag
from web.impl import lxml_components

from .utils import CONFIG_DIR, DB_FILE, log

try:
    # Must be imported be fore app is inited or it fails to import later
    from enaml.qt import QtWebEngineWidgets  # noqa: F401

    QT_WEBENGINE = True
except ImportError as e:
    warnings.warn(
        f"QtWebEngine is not available: {e}. " "Will fall back to basic html view"
    )
    QT_WEBENGINE = False

try:
    from enaml.qt import Qsci  # noqa: F401

    QT_QSCI = True
except ImportError as e:
    warnings.warn(f"QSci is not available: {e}. " "Theme editor will be disabled")
    QT_QSCI = False


def get_sys_config():
    from zerobooks.models.system import System

    return System


class ZeroApplication(QtApplication):
    #: Web component resolver
    web_resolver = Typed(ProxyResolver)
    queue = Typed(Queue, ())
    running = Bool()
    sys_config = ForwardTyped(get_sys_config, ())

    def __init__(self, appname=None):
        super().__init__(appname=appname or "zerobooks")

    def _default_web_resolver(self):
        return ProxyResolver(factories=lxml_components.FACTORIES)

    def resolve_proxy_class(self, declaration_class):
        """Resolve both html and qt elements."""
        if issubclass(declaration_class, Tag):
            resolver = self.web_resolver
            for base in declaration_class.mro():
                name = base.__name__
                cls = resolver.resolve(name)
                if cls is not None:
                    return cls
        return super().resolve_proxy_class(declaration_class)

    def write_to_websocket(self, websocket, message):
        self.deferred_call(websocket.write_message, message)

    def start(self):
        log.debug("ZeroApplication.start")
        try:
            self.running = True
            loop = asyncio.new_event_loop()
            with loop:
                loop.run_until_complete(self.main())
        except RuntimeError as e:
            log.debug(e)
        finally:
            log.debug("ZeroApplication.main exited")
            super().stop()

    @classmethod
    async def open_database(cls, url: Optional[str] = None):
        mgr = SQLModelManager.instance()
        if url is None:
            url = DB_FILE
        # If using mysql/postgres...
        # m = re.match(r"(.+)://(.+):(.*)@(.+):(\d+)/(.+)", url)
        # if not m:
        #    raise ValueError("Database url is invalid")
        # schema, user, pwd, host, port, db = m.groups()
        # engine = mgr.database = await create_engine(
        #     host=host,
        #     port=int(port),
        #     user=user,
        #     password=pwd,
        #     database=db,
        # )
        engine = mgr.database = await create_engine(url, isolation_level=None)
        return engine

    @classmethod
    async def close_database(cls):
        mgr = SQLModelManager.instance()
        if db := mgr.database:
            await db.terminate()
            await db.wait_closed()

    async def init_database(self):
        from zerobooks.models.system import System

        self.sys_config, _ = await System.objects.get_or_create()

    async def main(self):
        """Run any async deferred calls in the main ui loop."""
        await self.open_database()
        try:
            await self.init_database()
            while self.running:
                try:
                    task = self.queue.get(block=False)
                    if task is None:
                        break
                    await task
                except Empty:
                    await asyncio.sleep(0.1)
                except Exception as e:
                    # Handle errors here
                    raise e
        finally:
            await self.close_database()

    def stop(self):
        log.debug("ZeroApplication.stop")
        self.running = False

        #: HACK Improper shutdown
        import threading

        threading._shutdown_locks.clear()

    def deferred_call(self, callback, *args, **kwargs):
        if iscoroutine(callback):
            return self.queue.put(callback)
        return super().deferred_call(callback, *args, **kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        if iscoroutine(callback):
            return super().timed_call(ms, self.queue.put, callback)
        return super().timed_call(ms, callback, *args, **kwargs)


def init_logging():
    try:
        log_dir = os.path.join(CONFIG_DIR, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(
            filename=os.path.join(log_dir, "app.log"),
            encoding="utf-8",
            level=logging.DEBUG,
        )
        log.setLevel(logging.DEBUG)
        stdout = logging.StreamHandler()
        stdout.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
        stdout.setFormatter(formatter)
        log.addHandler(stdout)
    except Exception as e:
        warnings.warn(f"Failed to init logging: {e}")


def main():
    init_logging()
    asyncio.set_event_loop_policy(QEventLoopPolicy())

    enamlx.install()

    with enaml.imports():
        from .manifest import AppManifest

    from .workbench import ZeroWorkbench

    workbench = ZeroWorkbench()
    workbench.register(AppManifest())
    log.debug("App starting")
    workbench.run()


if __name__ == "__main__":
    main()
