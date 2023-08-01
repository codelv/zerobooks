"""
Copyright (c) 2023, Jairus Martin.

Distributed under the terms of the AGPL v3 License.

The full license is in the file LICENSE, distributed with this software.
"""
import re
from setuptools import setup, find_packages


# Read version
with open('zerobooks/__init__.py') as f:
    m = re.search(r'version = ["\'](.+)["\']', f.read(), re.MULTILINE)
    assert m is not None, 'Failed to read version'
    version = m.group(1)


setup(
    name='zerobooks',
    version=version,
    description='A non-saas invoicing software.',
    author="CodeLV",
    author_email="info@codelv.com",
    license="AGPLv3",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    url='https://codelv.com/projects/zerobooks/',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'enaml',
        'enamlx',
        'qtpy',
        'pyqt6',
        'weasyprint',
        'enaml-web',
        'atom-db',
        'asyncqtpy',
        'sqlalchemy',
        'alembic',
        'aiosqlite @ git+https://github.com/frmdstryr/aiosqlite.git@sa-support'
    ],
    extras_require={
      "webengine": "pyqt6-webengine",
      "editor": "pyqt6-qscintilla",
    },
    entry_points={
        'console_scripts': ['zerobooks = zerobooks.app:main'],
    },
)
