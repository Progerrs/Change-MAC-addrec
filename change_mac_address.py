#!/usr/bin/env python3

from subprocess import call, check_output
from optparse import OptionParser
from re import search


def get_arguments():
    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC address, use --help for more info.")
    return options


def change_mac(interface, new_mac_address):
    print("[+] Changing MAC address for:", interface, "to", new_mac_address)
    call(["sudo", "ifconfig", interface, "down"])
    call(["sudo", "ifconfig", interface, "hw", "ether", new_mac_address])
    call(["sudo", "ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_output = check_output(["ifconfig", interface])
    mac_address_search_result = search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_output))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
change_mac(options.interface, options.new_mac)
new_mac_address = get_current_mac(options.interface)
if new_mac_address == options.new_mac:
    print("[+] MAC address was successfully change to:", options.new_mac)
else:
    print("[-] MAC address didn't get change.")
