#
# ini_loader.py
# Copyright (C) 2024 laobamac
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configparser
import argparse
import plistlib
import os
import shutil
import requests

def ensure_plist_file_exists(plist_file):
    """确保 plist 文件存在"""
    if not os.path.exists(plist_file):
        print(f"Error: Plist file '{plist_file}' not found.")
        exit(1)

def edit_boot_args(plist_file, boot_args):
    """编辑 NVRAM 中的 boot-args"""
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    nvram_boot_args_key = '7C436110-AB2A-4BBB-A880-FE41995C9F82'
    current_boot_args = plist_data.get('NVRAM', {}).get(nvram_boot_args_key, {}).get('boot-args', '')

    if boot_args:
        # 如果 INI 文件中提供了 boot-args，则更新
        if current_boot_args != boot_args:
            plist_data['NVRAM'][nvram_boot_args_key] = {'boot-args': boot_args}
            with open(plist_file, 'wb') as f:
                plistlib.dump(plist_data, f, sort_keys=False)
            print(f"Updated boot-args to: '{boot_args}'")
        else:
            print("boot-args is already set to the desired value.")
    else:
        # 如果 INI 文件中 boot-args 为空，则保持不变
        print("No new boot-args provided, keeping the original value.")

def edit_kernel_add(plist_file, kextname, status):
    """编辑 Kernel 中的 Add 项"""
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    kernel_add = plist_data.get('Kernel', {}).get('Add', [])

    kext_path = f"{kextname}.kext"
    for item in kernel_add:
        if item.get('BundlePath') == kext_path:
            item['Enabled'] = (status == 1)
            break
    else:
        if status == 1:
            new_kext = {
                'Arch': 'Any',
                'BundlePath': kextname,
                'Comment': f'Added by ini_loader: {kextname}',
                'Enabled': True,
                'ExecutablePath': f"Contents/MacOS/{kextname}",
                'MaxKernel': '',
                'MinKernel': '',
                'PlistPath': f"Contents/Info.plist"
            }
            kernel_add.append(new_kext)

    with open(plist_file, 'wb') as f:
        plist_data['Kernel']['Add'] = kernel_add
        plistlib.dump(plist_data, f, sort_keys=False)

def edit_acpi_add(plist_file, ssdtname, status):
    """编辑 ACPI 中的 Add 项"""
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    acpi_add = plist_data.get('ACPI', {}).get('Add', [])

    ssdt_path = f"{ssdtname}.aml"
    for item in acpi_add:
        if item.get('Path') == ssdt_path:
            item['Enabled'] = (status == 1)
            break
    else:
        if status == 1:
            new_ssdt = {
                'Comment': f'Added by ini_loader: {ssdtname}',
                'Enabled': True,
                'Path': ssdt_path
            }
            acpi_add.append(new_ssdt)

    with open(plist_file, 'wb') as f:
        plist_data['ACPI']['Add'] = acpi_add
        plistlib.dump(plist_data, f, sort_keys=False)

def edit_quirks(plist_file, dict_code, quirkname, status):
    """编辑 Booter、Kernel 或 ACPI 中的 Quirks 项"""
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    dict_name = 'ACPI' if dict_code == 1 else 'Booter' if dict_code == 2 else 'Kernel'
    dict_data = plist_data.get(dict_name, {})

    quirks_data = dict_data.get('Quirks', {})
    quirks_data[quirkname] = (status == 1)

    with open(plist_file, 'wb') as f:
        plist_data[dict_name]['Quirks'] = quirks_data
        plistlib.dump(plist_data, f, sort_keys=False)

def main(inipath, plistpath=None):
    """主函数，根据 INI 配置文件修改 config.plist"""
    config = configparser.ConfigParser()
    config.read(inipath)

    # 如果没有指定 plistpath，则使用默认路径
    if not plistpath:
        plistpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp', 'EFI', 'OC', 'config.plist')
    ensure_plist_file_exists(plistpath)

    if 'Kernel' in config:
        for kextname, status in config['Kernel'].items():
            edit_kernel_add(plistpath, kextname, int(status))

    if 'ACPI' in config:
        for ssdtname, status in config['ACPI'].items():
            edit_acpi_add(plistpath, ssdtname, int(status))

    if 'BQ' in config:
        for quirkname, status in config['BQ'].items():
            edit_quirks(plistpath, 2, quirkname, int(status))

    if 'KQ' in config:
        for quirkname, status in config['KQ'].items():
            edit_quirks(plistpath, 3, quirkname, int(status))

    if 'AQ' in config:
        for quirkname, status in config['AQ'].items():
            edit_quirks(plistpath, 1, quirkname, int(status))

    if 'NVRAM' in config:
        boot_args = config['NVRAM'].get('boot-args', '')
        edit_boot_args(plistpath, boot_args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load INI configuration and modify config.plist")
    parser.add_argument("inipath", type=str, help="Path to the INI configuration file")
    parser.add_argument("-p", "--plistpath", type=str, help="Path to the config.plist file", default=None)
    args = parser.parse_args()

    main(args.inipath, args.plistpath)
