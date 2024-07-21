import argparse
import plistlib
# powered by laobamac,请遵循GPLv3开源协议
import configparser
import os

# INI 文件注释
copyright_notice = "# Powered by laobamac, please comply with the GPLv3 open source license\n"

def plist_to_ini(plist_path):
    with open(plist_path, 'rb') as f:
        plist_data = plistlib.load(f)

    config = configparser.ConfigParser()

    def quirks_to_configparser(section_data, section_name):
        for quirk_name, quirk_value in section_data.items():
            config[section_name][f"{quirk_name}"] = str(quirk_value)

    kernel_add = plist_data.get('Kernel', {}).get('Add', [])
    for kext in kernel_add:
        kext_name = os.path.basename(kext['BundlePath']).split('.')[0]
        config['Kernel'][kext_name] = str(kext['Enabled'])

    acpi_add = plist_data.get('ACPI', {}).get('Add', [])
    for ssdt in acpi_add:
        ssdt_name = os.path.basename(ssdt['Path']).split('.')[0]
        config['ACPI'][ssdt_name] = str(ssdt['Enabled'])

    quirks_sections = ['Booter', 'Kernel', 'ACPI']
    for section in quirks_sections:
        if section in plist_data:
            quirks_data = plist_data[section].get('Quirks', {})
            quirks_to_configparser(quirks_data, section)

    return config

def save_config_to_ini(config, output_path):
    with open(output_path, 'w') as f:
        f.write(copyright_notice)
        config.write(f)

def main(plist_path, output_path=None):
    # 如果没有指定输出路径，则将 INI 文件保存到 plist 同目录
    if not output_path:
        output_dir = os.path.dirname(plist_path)
        output_path = os.path.join(output_dir, "config.ini")

    config = plist_to_ini(plist_path)
    save_config_to_ini(config, output_path)
    print(f"INI file has been created at: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert config.plist to INI configuration file.")
    parser.add_argument("configpath", type=str, help="Path to the config.plist file.")
    parser.add_argument("-o", "--output", type=str, help="Output INI file path.", default=None)
    args = parser.parse_args()

    main(args.configpath, args.output)
