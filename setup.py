#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="systemd-wait",
    version="0.1",
    description="Wait for a systemd unit to enter a specific state",
    py_modules=["systemd_wait"],
    entry_points={
        'console_scripts': [
            'systemd-wait = systemd_wait:main',
        ],
    },
    install_requires=[
        "PyGObject>=3.0",
    ],
    requires=[
        # dbus_python is weird and can't go in install_requires.  It
        # usually needs to be installed from a distro package, as
        # pypi/pip installs of it are troublesome.
        "dbus_python",
    ],
    author="Steven Allen",
    author_email="steven@stebalien.com",
    url="https://github.com/Stebalien/systemd-wait",
)
