# ini_loader.py
# Copyright (C) 2024 laobamac
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# 求求你们了，某些同行别老污蔑有后门了，laoba脆弱啊5555555555
import os
import shutil
import configparser
import argparse
import plistlib

def ensure_temp_dir_exists():
    """确保 temp 目录存在"""
    temp_path = 'temp'
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

def edit_kernel_add(action, kextname, status, plist_file='temp/config.plist'):
    """编辑 Kernel 中的 Add 项"""
    ensure_temp_dir_exists()

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 找到 Kernel 下的 Add 键
    kernel_add = plist_data.get('Kernel', {}).get('Add', [])

    kext_path = f"{kextname}.kext"

    if action == 1:
        # 添加并启用 kext
        new_kext = {
            'Arch': 'Any',
            'BundlePath': kext_path,
            'Comment': f'SimpleHac {kextname}',
            'Enabled': True,
            'ExecutablePath': f"Contents/MacOS/{kextname}",
            'MaxKernel': '',
            'MinKernel': '',
            'PlistPath': f"Contents/Info.plist"
        }
        kernel_add.append(new_kext)
        print(f"Added and enabled {kextname}")
    elif action == 2:
        # 删除 kext
        kernel_add = [item for item in kernel_add if item.get('BundlePath') != kext_path]
        print(f"Removed {kextname}")
    elif action == 3:
        # 禁用 kext
        for item in kernel_add:
            if item.get('BundlePath') == kext_path:
                item['Enabled'] = False
                print(f"Disabled {kextname}")
                break
    elif action == 4:
        # 启用 kext
        for item in kernel_add:
            if item.get('BundlePath') == kext_path:
                item['Enabled'] = True
                print(f"Enabled {kextname}")
                break

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        plist_data['Kernel']['Add'] = kernel_add
        plistlib.dump(plist_data, f, sort_keys=False)

def edit_acpi_add(action, ssdtname, status, plist_file='temp/config.plist'):
    """编辑 ACPI 中的 Add 项"""
    ensure_temp_dir_exists()

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 找到 ACPI 下的 Add 键
    acpi_add = plist_data.get('ACPI', {}).get('Add', [])

    ssdt_path = f"{ssdtname}.aml"

    if action == 1:
        # 添加并启用 ACPI 表
        new_ssdt = {
            'Comment': f'Custom SSDT for {ssdtname}',
            'Enabled': True,
            'Path': ssdt_path
        }
        acpi_add.append(new_ssdt)
        print(f"Added and enabled {ssdtname}")
    elif action == 2:
        # 删除 ACPI 表
        acpi_add = [item for item in acpi_add if item.get('Path') != ssdt_path]
        print(f"Removed {ssdtname}")
    elif action == 3:
        # 禁用 ACPI 表
        for item in acpi_add:
            if item.get('Path') == ssdt_path:
                item['Enabled'] = False
                print(f"Disabled {ssdtname}")
                break
    elif action == 4:
        # 启用 ACPI 表
        for item in acpi_add:
            if item.get('Path') == ssdt_path:
                item['Enabled'] = True
                print(f"Enabled {ssdtname}")
                break

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        plist_data['ACPI']['Add'] = acpi_add
        plistlib.dump(plist_data, f, sort_keys=False)

def edit_quirks(dict_code, quirkname, status, plist_file='temp/config.plist'):
    """编辑 Booter 或 ACPI 或 Kernel 中的 Quirks 项"""
    ensure_temp_dir_exists()

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    dict_name = 'ACPI' if dict_code == 1 else 'Booter' if dict_code == 2 else 'Kernel'

    if dict_name not in plist_data:
        print(f"Error: '{dict_name}' not found in plist data.")
        return

    dict_data = plist_data[dict_name]

    if 'Quirks' not in dict_data:
        print(f"Error: 'Quirks' not found in {dict_name}.")
        return

    quirks_data = dict_data['Quirks']

    if quirkname not in quirks_data:
        print(f"Error: Quirk '{quirkname}' not found in {dict_name} Quirks.")
        return

    # 设置 Quirk 的状态
    quirks_data[quirkname] = (status == 1)

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        plist_data[dict_name]['Quirks'] = quirks_data
        plistlib.dump(plist_data, f, sort_keys=False)
    print(f"Quirk '{quirkname}' in {dict_name} has been {'enabled' if status == 1 else 'disabled'}.")

def load_config(inipath):
    """加载INI配置文件"""
    config = configparser.ConfigParser()
    config.read(inipath)
    return config

def process_kexts_and_ssdts(config, section):
    """处理Kernel和ACPI部分的Kext和SSDT列表"""
    for item, status in config.items(section):
        if status.lower() == 'true':
            edit_kernel_add(1, item, 1)  # 添加并启用
            edit_acpi_add(1, item, 1)    # 添加并启用
        else:
            edit_kernel_add(2, item, 2)  # 删除
            edit_acpi_add(2, item, 2)    # 删除

def process_quirks(config, section, dict_code):
    """处理Booter、Kernel、ACPI中的Quirks"""
    for quirkname, status in config.items(section):
        if status.lower() == 'false':
            edit_quirks(dict_code, quirkname, 2)  # 禁用
        else:
            edit_quirks(dict_code, quirkname, 1)  # 启用

def main(inipath):
    """主函数，根据INI配置文件修改config.plist"""
    ensure_temp_dir_exists()

    # 加载配置文件
    config = load_config(inipath)

    # 处理Kernel部分的Kext和SSDT列表
    if 'Kernel' in config:
        process_kexts_and_ssdts(config, 'Kernel')

    # 处理ACPI部分的Kext和SSDT列表
    if 'ACPI' in config:
        process_kexts_and_ssdts(config, 'ACPI')

    # 处理BQ部分的Booter Quirks
    if 'BQ' in config:
        process_quirks(config, 'BQ', 2)  # dict_code为2代表Booter

    # 处理KQ部分的Kernel Quirks
    if 'KQ' in config:
        process_quirks(config, 'KQ', 3)  # dict_code为3代表Kernel

    # 处理AQ部分的ACPI Quirks
    if 'AQ' in config:
        process_quirks(config, 'AQ', 1)  # dict_code为1代表ACPI

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto create EFI for Hackintosh.")
    parser.add_argument("inipath", type=str, help="Path to the INI configuration file
