# ba_quirk_editor.py
# powered by laobamac,请遵循GPLv3开源协议
import plistlib
import argparse
import os

def edit_quirks(dict_code, quirkname, status, plist_file='temp/config.plist'):
    """
    编辑 Booter 或 ACPI 中的 Quirks 项。

    :param dict_code: 字典代码，1 表示 ACPI，2 表示 Booter
    :param quirkname: Quirk 的名称
    :param: Quirk 的名称
    :param status: 状态，1 表示启用，2 表示禁用
    :param plist_file: plist 文件路径
    """
    # 确保 temp 目录存在
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 根据 dict_code 找到对应的字典键
    dict_name = 'ACPI' if dict_code == 1 else 'Booter'
    if dict_name not in plist_data:
        print(f"Error: '{dict_name}' not found in plist data.")
        return

    dict_data = plist_data[dict_name]

    # 找到 Quirks 键
    if 'Quirks' not in dict_data:
        print(f"Error: 'Quirks' not found in {dict_name}.")
        return

    quirks_data = dict_data['Quirks']

    # 检查 Quirk 是否存在
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

def main():
    parser = argparse.ArgumentParser(description="Edit Quirks in Booter or ACPI in a plist file.")
    parser.add_argument("dict_code", type=int, choices=[1, 2], help="Dictionary code: 1 for ACPI, 2 for Booter")
    parser.add_argument("quirkname", type=str, help="The name of the quirk")
    parser.add_argument("status", type=int, choices=[1, 2], help="Status: 1 to enable, 2 to disable")

    args = parser.parse_args()

    try:
        edit_quirks(args.dict_code, args.quirkname, args.status)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
