# boot_args_editor.py
# powered by laobamac,请遵循GPLv3开源协议
import plistlib
import argparse
import os
from shutil import copyfile

def edit_boot_args(action, value, plist_file='temp/config.plist'):
    """
    编辑 NVRAM 中的 boot-args。

    :param action: 操作类型，1 表示读取，2 表示添加，3 表示删除
    :param value: 要添加或删除的值
    :param plist_file: plist 文件路径
    """
    # 确保 temp 目录存在
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 找到 NVRAM 下的 Add 键
    nvram_data = plist_data.get('NVRAM', {})

    # 找到 boot-args
    boot_args_key = '7C436110-AB2A-4BBB-A880-FE41995C9F82'
    boot_args = nvram_data.get(boot_args_key, {}).get('boot-args', '')

    if action == 1:
        # 读取现有的 boot-args 并输出
        print(f"Current boot-args: {boot_args}")
    elif action == 2:
        # 添加 boot-args
        if boot_args:
            boot_args += ' '
        boot_args += value.strip()
        print(f"New boot-args: {boot_args}")
    elif action == 3:
        # 删除 boot-args
        args_list = boot_args.split(' ')
        new_args_list = [arg for arg in args_list if arg != value]
        boot_args = ' '.join(new_args_list).strip()
        print(f"New boot-args: {boot_args}")

    # 更新 NVRAM 数据
    nvram_data[boot_args_key] = {'boot-args': boot_args}
    plist_data['NVRAM'] = nvram_data

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        plistlib.dump(plist_data, f, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description="Edit boot-args in NVRAM in a plist file.")
    parser.add_argument("action", type=int, choices=[1, 2, 3], help="Action: 1 to read, 2 to add, 3 to remove")
    parser.add_argument("value", type=str, help="The value to add or remove")

    args = parser.parse_args()

    try:
        edit_boot_args(args.action, args.value)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
