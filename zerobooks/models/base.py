"""
Copyright (c) 2023, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
from datetime import datetime
from uuid import uuid4

from atom.api import Str, Typed
from atomdb.sql import SQLModel


class BaseModel(SQLModel):
    #: UUID
    uuid = Str(factory=lambda: str(uuid4().hex)).tag(length=36, unique=True)
    created = Typed(datetime, factory=datetime.now)
    updated = Typed(datetime, factory=datetime.now)

    async def save(self, *args, **kwargs):
        self.updated = datetime.now()
        await super().save(*args, **kwargs)

    class Meta:
        abstract = True
