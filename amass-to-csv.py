#!/usr/bin/env python3

# By Robert Gilbert (amroot.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import csv
import json
import sys

if len(sys.argv) < 3:
    exit('Usage: ' + sys.argv[0] + ' amass-in-file.json amass-out-file.csv')

amass = []
for line in open(sys.argv[1], 'r'):
    amass.append(json.loads(line))

csv_file = str(sys.argv[2])

with open(csv_file, 'w', newline='') as csv_file:
    amasswriter = csv.writer(csv_file, dialect='excel')
    amasswriter.writerow(['name', 'domain', 'ip', 'cidr',
                          'asn', 'desc', 'tag', 'source'])

    for count, row in enumerate(amass):

        name = row['name']
        domain = row['domain']
        addresses = row['addresses']
        ip = []
        cidr = []
        asn = []
        desc = []
        tag = ''
        source = []

        for address in addresses:
            ip.append(address['ip'])
            cidr.append(address['cidr'])
            asn.append(str(address['asn']))
            desc.append(address['desc'])

        tag = row['tag']

        # the old format did not use a [list] for source
        if 'sources' in row:
            source = row['sources']
        elif 'source' in row:
            source.append(row['source'])

        if '-n' in sys.argv:
            for i, d in enumerate(ip):
                amasswriter.writerow([name,
                                      domain,
                                      d,
                                      cidr[i],
                                      asn[i],
                                      desc[i],
                                      tag,
                                      source[0]])
        else:
            amasswriter.writerow([name,
                                  domain,
                                  '\r\n'.join(ip),
                                  '\r\n'.join(cidr),
                                  '\r\n'.join(asn),
                                  '\r\n'.join(desc),
                                  tag,
                                  '\r\n'.join(source)])


print('[i] Wrote ' + str(count) + ' lines')
print('[+] Done')
