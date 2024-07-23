import plistlib
import configparser
from argparse import ArgumentParser
# powered by laobamac,请遵循GPLv3开源协议
# 阿巴阿巴阿巴阿巴awawawawa
# 解析命令行参数
parser = ArgumentParser(description='Update a config.plist file with settings from an INI configuration file.')
parser.add_argument('configpath', help='Path to the config.plist file')
parser.add_argument('inipath', help='Path to the INI configuration file')
args = parser.parse_args()

# 读取 INI 文件
config = configparser.ConfigParser()
config.read(args.inipath)

# 读取 plist 文件
plist_data = plistlib.load(open(args.configpath, 'rb'))

# 根据 INI 更新 plist 中的数据
def update_plist_with_ini(plist_data, config):
    # 清空并添加新的 ACPI 表
    plist_data['ACPI'] = plist_data.get('ACPI', {})
    plist_data['ACPI']['Add'] = []
    for ssdt, enabled in config['SSDTs'].items():
        if enabled.lower() == 'true':
            plist_data['ACPI']['Add'].append({'Path': ssdt + '.aml', 'Enabled': True})

    # 清空并添加新的 Kexts 列表
    plist_data['Kernel'] = plist_data.get('Kernel', {})
    plist_data['Kernel']['Add'] = []
    for kext, enabled in config['Kexts'].items():
        if enabled.lower() == 'true':
            plist_data['Kernel']['Add'].append({'BundlePath': kext + '.kext', 'Enabled': True})

    # 清空并添加新的 NVRAM 条目
    plist_data['NVRAM'] = plist_data.get('NVRAM', {})
    plist_data['NVRAM']['Add'] = {}
    for key, value in config['NVRAM'].items():
        parts = key.split('.')
        if len(parts) == 2:
            plist_data['NVRAM']['Add'][parts[0]] = plist_data['NVRAM']['Add'].get(parts[0], {})
            plist_data['NVRAM']['Add'][parts[0]][parts[1]] = value

    # 清空并添加新的 PlatformInfo 条目
    plist_data['PlatformInfo'] = {}
    for key, value in config['PlatformInfo'].items():
        if key == 'Generic':
            plist_data['PlatformInfo']['Generic'] = {}
            for subkey, subvalue in value.items():
                plist_data['PlatformInfo']['Generic'][subkey] = subvalue
        else:
            plist_data['PlatformInfo'][key] = value

    # 清空并添加新的 DeviceProperties 条目
    plist_data['DeviceProperties'] = plist_data.get('DeviceProperties', {})
    plist_data['DeviceProperties']['Add'] = {}
    for section in config.sections():
        if section.startswith('DeviceProperties'):
            device_path = section.split('DeviceProperties')[1].strip()
            plist_data['DeviceProperties']['Add'][device_path] = {}
            for key, value in config[section].items():
                plist_data['DeviceProperties']['Add'][device_path][key] = value

# 调用更新函数
update_plist_with_ini(plist_data, config)

# 写入更新后的 plist 文件
with open(args.configpath, 'wb') as f:
    plistlib.dump(plist_data, f)

print(f"The plist file at {args.configpath} has been updated with settings from {args.inipath}")
