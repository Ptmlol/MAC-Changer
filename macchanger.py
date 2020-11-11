#!usr/bin/env/ python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC adress for.")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter the new mac for interface")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("You need to specify the interface! Use -h for help.")
    elif not options.new_mac:
        parser.error("You need to specify the new MAC! Use -h for help.")
    else:
        return options


def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_curent_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_adress_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_adress_search_result:
        return mac_adress_search_result.group(0)
    else:
        return "Could not read MAC adress."


option = get_arguments()
current_mac = get_curent_mac(option.interface)
print("Old MAC: " + str(current_mac))
change_mac(option.interface, option.new_mac)
current_mac = get_curent_mac(option.interface)
if current_mac == option.new_mac:
    print("MAC adress succesfully changed to: " + option.new_mac)
else:
    print("MAC did not get changed")
