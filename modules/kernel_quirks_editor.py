# kernel_quirks_editor.py
# powered by laobamac, 请遵循GPLv3开源协议
import plistlib
import argparse
import os
# 将配置文件置于temp/config.plist
def edit_kernel_quirk(quirkname, status, plist_file='temp/config.plist', output_file='temp/config_modified.plist'):
    """
    编辑 Kernel 中的 Quirks 项。

    :param quirkname: 要编辑的 Quirks 名称
    :param status: 状态，1 表示启用（true），2 表示禁用（false）
    :param plist_file: 输入的 plist 文件名
    :param output_file: 输出的 plist 文件名
    """
    # 检查状态参数
    if status not in (1, 2):
        raise ValueError("status must be 1 (enable) or 2 (disable)")

    # 确保 temp 目录存在
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 找到 Kernel 下的 Quirks 键
    kernel_quirks = plist_data.get('Kernel', {}).get('Quirks', {})

    # 设置 Quirks 项的状态
    if quirkname in kernel_quirks:
        kernel_quirks[quirkname] = (status == 1)
    else:
        raise KeyError(f"Quirk '{quirkname}' not found in Kernel Quirks")

    # 保存修改后的 plist 文件
    with open(output_file, 'wb') as f:
        plistlib.dump(plist_data, f, sort_keys=False)

    print(f"Quirk '{quirkname}' has been {'enabled' if status == 1 else 'disabled'}.")

def main():
    parser = argparse.ArgumentParser(description="Edit Kernel Quirks in a plist file.")
    parser.add_argument("quirkname", type=str, help="The name of the quirk to edit")
    parser.add_argument("status", type=int, choices=[1, 2], help="Status: 1 to enable, 2 to disable")

    args = parser.parse_args()

    try:
        edit_kernel_quirk(args.quirkname, args.status)
    except Exception as e:
        print(f"Error: {e}")
# python kernel_quirks_editor.py quirkname status
if __name__ == "__main__":
    main()