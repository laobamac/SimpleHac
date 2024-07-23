import plistlib
import configparser
from argparse import ArgumentParser
# powered by laobamac,请遵循GPLv3开源协议
# 解析命令行参数
parser = ArgumentParser(description='Update a config.plist file with settings from an INI configuration file.')
parser.add_argument('configpath', help='Path to the config.plist file')
parser.add_argument('inipath', help='Path to the INI configuration file')
args = parser.parse_args()

# 读取 INI 文件
config = configparser.ConfigParser()
config.read(args.inipath)

# 读取 plist 文件
plist_path = args.configpath
with open(plist_path, 'rb') as f:
    plist_data = plistlib.load(f)

# 根据 INI 更新 plist 中的数据
def update_plist_with_ini(plist_data, config):
    # 清空并添加新的 Quirks 信息
    for quirk_type in ['ACPI', 'Booter', 'Kernel', 'UEFI']:
        plist_data[quirk_type] = {'Quirks': {}}
        for key, value in config.items(f"{quirk_type}.Quirks"):
            plist_data[quirk_type]['Quirks'][key] = value.strip() == 'true'

    # 清空并添加新的 Kexts 信息
    plist_data['Kernel'] = {'Add': []}
    for kext_path, enabled in config.items('Kexts'):
        plist_data['Kernel']['Add'].append({'BundlePath': kext_path, 'Enabled': enabled.strip() == 'true'})

    # 清空并添加新的 SSDTs 信息
    plist_data['ACPI'] = {'Add': []}
    for ssdt_path, enabled in config.items('SSDTs'):
        plist_data['ACPI']['Add'].append({'Path': ssdt_path, 'Enabled': enabled.strip() == 'true'})

    # 更新 NVRAM boot-args
    nvram_boot_args = config.get('NVRAM', 'boot-args', fallback="")
    plist_data['NVRAM'] = {'Add': {'7C436110-AB2A-4BBB-A880-FE41995C9F82': {'boot-args': nvram_boot_args}}}

    # 清空并添加新的 PlatformInfo 信息
    plist_data['PlatformInfo'] = {}
    for key, value in config.items('PlatformInfo'):
        plist_data['PlatformInfo'][key] = value

# 调用更新函数
update_plist_with_ini(plist_data, config)

# 写入更新后的 plist 文件
with open(plist_path, 'wb') as f:
    plistlib.dump(plist_data, f)

print(f"The plist file at {plist_path} has been updated with settings from {args.inipath}")
