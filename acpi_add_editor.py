# acpi_add_editor.py
# powered by laobamac, 请遵循GPLv3开源协议
import plistlib
import argparse
import os

def edit_acpi_add(action, ssdtname, status, plist_file='temp/config.plist'):
    """
    编辑 ACPI 中的 Add 项。

    :param action: 操作类型，1 表示添加 ACPI 表，2 表示删除 ACPI 表
    :param ssdtname: ACPI 表的名称（不包含扩展名）
    :param status: 状态，1 表示启用，2 表示禁用（仅在添加时考虑）
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

    # 根据 action 执行操作
    if action == 1:
        # 添加 ACPI 表
        ssdt_path = f"{ssdtname}.aml"
        new_ssdt = {
            'Comment': f'Custom SSDT for {ssdtname}',
            'Enabled': (status == 1),
            'Path': ssdt_path
        }
        acpi_add.append(new_ssdt)
        print(f"Added {ssdtname} with status {('enabled' if status == 1 else 'disabled')}")
    elif action == 2:
        # 删除 ACPI 表
        acpi_add = [item for item in acpi_add if item.get('Path') != f"{ssdtname}.aml"]
        print(f"Removed {ssdtname}")

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        plist_data['ACPI']['Add'] = acpi_add
        plistlib.dump(plist_data, f, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description="Edit ACPI Add in a plist file.")
    parser.add_argument("action", type=int, choices=[1, 2], help="Action: 1 to add, 2 to remove")
    parser.add_argument("ssdtname", type=str, help="The name of the SSDT")
    parser.add_argument("status", type=int, choices=[1, 2], help="Status: 1 to enable, 2 to disable (only for adding)")

    args = parser.parse_args()

    try:
        edit_acpi_add(args.action, args.ssdtname, args.status)
    except Exception as e:
        print(f"Error: {e}")
# python acpi_add_editor.py action ssdttime status
if __name__ == "__main__":
    main()