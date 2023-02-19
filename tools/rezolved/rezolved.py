#!/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

import logging
import json
import ipaddress
import subprocess
from pydbus import SystemBus

bus = SystemBus()
resolve1 = bus.get('org.freedesktop.resolve1', '/org/freedesktop/resolve1')

try:
    devices = json.loads(subprocess.run(['ip', '--json', 'link', 'show'], capture_output = True, check = True).stdout)
    networks = json.loads(subprocess.run(['zerotier-cli', '-j', 'listnetworks'], capture_output = True, check = True).stdout)
except subprocess.CalledProcessError as err:
    output = (err.stderr or err.stdout).decode()
    raise RuntimeError(f'Failed to list devices or networks: {output}') from err

for net in networks:
    try:
        dev = next((dev for dev in devices if dev['ifname'] == net['portDeviceName']), [None])
    except:
        logging.error(f'Cannot find network device "{net["portDeviceName"]}"')
        continue

    if net['allowDNS'] and net['dns']['servers']:
        addresses = []

        for server in net['dns']['servers']:
            addr = ipaddress.ip_address(server)

            if addr.version == 4:
                addresses.append([2, addr.packed]) # AF_INET
            elif addr.version == 6:
                addresses.append([10, addr.packed]) # AF_INET6

        resolve1.SetLinkDNS(dev['ifindex'], addresses)
        resolve1.SetLinkDomains(dev['ifindex'], [(net['dns']['domain'], False)])
    else:
        resolve1.SetLinkDNS(dev['ifindex'], [])
        resolve1.SetLinkDomains(dev['ifindex'], [])
