# acpi_add_editor.py
# powered by laobamac, 请遵循GPLv3开源协议
import plistlib
import argparse
import os

def edit_acpi_add(action, ssdtname, status, plist_file='temp/config.plist'):
    """
    编辑 ACPI 中的 Add 项。

    :param action: 操作类型，1 表示添加 ACPI 表，2 表示删除 ACPI 表，3 表示禁用 ACPI 表，4 表示启用 ACPI 表
    :param ssdtname: ACPI 表的名称（不包含扩展名）
    :param status: 状态，1 表示启用，2 表示禁用
    :param plist_file: plist 文件路径
    """
    # 确保 temp 目录存在
    if not os.path.exists('temp'):
        os.makedirs('temp')

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

def main():
    parser = argparse.ArgumentParser(description="Edit ACPI Add in a plist file.")
    parser.add_argument("action", type=int, choices=[1, 2, 3, 4], help="Action: 1 to add and enable, 2 to remove, 3 to disable, 4 to enable")
    parser.add_argument("ssdtname", type=str, help="The name of the SSDT")
    args = parser.parse_args()

    try:
        edit_acpi_add(args.action, args.ssdtname, 1 if args.action in (1, 4) else 2)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()