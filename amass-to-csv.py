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

from argparse import ArgumentParser
from csv import writer as csv_writer
from json import loads as json_loads

def get_args():
    parser = ArgumentParser()    
    parser.add_argument('-i', '--amass_in', 
        help='Path to the Amass input JSON file.',
        required=True)
    parser.add_argument('-o', '--csv_out', 
        help='Path to output CSV file.',
        required=True)
    parser.add_argument('-ip', '--by_ip',
        action='store_true',
        help=('Create a new line for each IP address. '
        'Default is new line for each subdomain and a cell with all associated '
        'IP address'))
    return parser


def print_color(message, code, return_color = False):
    """Prints or returns pretty colors -_o
    Param message (str): the message to print
    Param code (str): e = red, i = blue, g = green, w = yellow
    Param return_color (bool): returns the message and color code 
    rather than printing it directly.
    """
    # Errors red
    if code == "e":
        if return_color:
            return "\033[91m[!] " + message + "\033[0m"
        print("\033[91m[!] " + message + "\033[0m")
    
    # Information blue
    if code == "i":
        if return_color:
            return "\033[95m[*] " + message + "\033[0m"
        print("\033[95m[*] " + message + "\033[0m")
    
    # Good green
    if code == "g":
        if return_color:
            return "\033[92m[+] " + message + "\033[0m"
        print("\033[92m[+] " + message + "\033[0m")
    
    # Warning yellow
    if code == "w":
        if return_color:
            return "\033[93m[*] " + message + "\033[0m"
        print("\033[93m[*] " + message + "\033[0m")


def amass_csv(amass_in, csv_out, by_ip=False):
    """ Returns Amass results in Excell compatable CSV format
    Param amass_in (str): the Amass data to convert to CSV
    Param csv_out (str): the path to the CSV output file
    """
    amass = []
    with open(amass_in, 'r') as fh:
        for line in fh:
            amass.append(json_loads(line))

    with open(csv_out, 'w', newline='') as fh:
        amasswriter = csv_writer(fh, dialect='excel')
        amasswriter.writerow(['name', 'domain', 'ip', 'cidr',
                            'asn', 'desc', 'tag', 'source'])

        write_count = 0
        for row in amass:
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

            if by_ip:
                for i, d in enumerate(ip):
                    amasswriter.writerow([name,
                        domain,
                        d,
                        cidr[i],
                        asn[i],
                        desc[i],
                        tag,
                        source[0]])
                    write_count += 1
            else:
                amasswriter.writerow([name,
                    domain,
                    '\r\n'.join(ip),
                    '\r\n'.join(cidr),
                    '\r\n'.join(asn),
                    '\r\n'.join(desc),
                    tag,
                    '\r\n'.join(source)])
                write_count += 1
    return write_count


def main():
    args = get_args().parse_args()
    print_color('Starting your bidding.', 'g')
    count = amass_csv(args.amass_in, args.csv_out, args.by_ip)
    print_color('Wrote ' + str(count) + ' Amass lines', 'i')
    print_color('Done', 'g')

if __name__ == "__main__":
    main()