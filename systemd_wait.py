#!/usr/bin/env python3
# encoding: utf-8

# A simple tool to wait for a systemd unit to enter a specific state.
# Copyright (C) 2013 Steven Allen
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import binascii
import re

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

UNIT_INTERFACE = 'org.freedesktop.systemd1.Unit'
UNIT_STATES = [
    "active",
    "reloading",
    "inactive",
    "failed",
    "activating",
    "deactivating",
]

UNIT_REGEX = re.compile('[^A-Za-z0-9]')

DBusGMainLoop(set_as_default=True)

EVENT_LOOP = GLib.MainLoop()


def wait(bus, unit, target_states):
    state = None

    path = "/org/freedesktop/systemd1/unit/" + UNIT_REGEX.sub(
        lambda x: "_" + binascii.hexlify(bytes(x.group(0), 'utf-8')).decode('utf-8'),
        unit
    )

    unit_int = dbus.Interface(
        bus.get_object('org.freedesktop.systemd1',
                       path),
        dbus_interface=dbus.PROPERTIES_IFACE
    )

    def get_active_state():
        """Get the current state of the unit."""
        return unit_int.Get(UNIT_INTERFACE, "ActiveState")

    def handler(interface, changed, invalidated):
        """Handle PropertiesChanged events."""
        nonlocal state
        if interface == UNIT_INTERFACE:
            if "ActiveState" in invalidated:
                state = get_active_state()
            elif "ActiveState" in changed:
                state = changed['ActiveState']
            if state in target_states:
                EVENT_LOOP.quit()

    unit_int.connect_to_signal('PropertiesChanged', handler)

    manager_int = dbus.Interface(
        bus.get_object('org.freedesktop.systemd1',
                       '/org/freedesktop/systemd1'),
        dbus_interface="org.freedesktop.systemd1.Manager"
    )

    manager_int.Subscribe()

    state = get_active_state()
    if state not in target_states:
        EVENT_LOOP.run()

    manager_int.Unsubscribe()

    # state was reassigned in handler()
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quiet", help="Don't print resulting state",
                        action="store_true")
    parser.add_argument("--user", help="Connect to user service manager",
                        action="store_true")
    parser.add_argument("unit", help="Unit for which to wait")
    parser.add_argument("state", help="States for which to wait",
                        choices=UNIT_STATES, nargs='+')

    args = parser.parse_args()
    bus = dbus.SessionBus() if args.user else dbus.SystemBus()
    state = wait(bus, args.unit, args.state)
    if not args.quiet:
        print(state)


if __name__ == '__main__':
    main()
