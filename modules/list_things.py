# list_things.py
# powered by laobamac,请遵循GPLv3开源协议
import plistlib
import argparse
import os

def list_acpi_add(plist_file='temp/config.plist'):
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    acpi_add = plist_data.get('ACPI', {}).get('Add', [])
    ssdts = [item['Path'] for item in acpi_add if 'Path' in item]
    return '\n'.join(ssdts)

def list_kernel_add(plist_file='temp/config.plist'):
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    kernel_add = plist_data.get('Kernel', {}).get('Add', [])
    kexts = [item['BundlePath'] for item in kernel_add if 'BundlePath' in item]
    return '\n'.join(kexts)

def list_uefi_drivers(plist_file='temp/config.plist'):
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    uefi_drivers = plist_data.get('UEFI', {}).get('Drivers', [])
    drivers = [item['Path'] for item in uefi_drivers if 'Path' in item]
    return '\n'.join(drivers)

def main(dictname):
    plist_file = 'temp/config.plist'
    
    if not os.path.exists(plist_file):
        print("Error: plist file not found.")
        return

    if dictname == '1':
        print(list_acpi_add(plist_file))
    elif dictname == '2':
        print(list_kernel_add(plist_file))
    elif dictname == '3':
        print(list_uefi_drivers(plist_file))
    else:
        print("Invalid dictname. Use 1 for ACPI, 2 for Kernel, or 3 for UEFI.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List items in a plist file.")
    parser.add_argument("dictname", type=str, choices=['1', '2', '3'], help="Dictionary name: 1 for ACPI, 2 for Kernel, 3 for UEFI")
    args = parser.parse_args()

    main(args.dictname)
