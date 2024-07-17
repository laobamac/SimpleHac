# kernel_add_editor.py
# powered by laobamac, 请遵循GPLv3开源协议
import plistlib
import argparse
import os

def edit_kernel_add(action, kextname, status, plist_file='temp/config.plist'):
    """
    编辑 Kernel 中的 Add 项。

    :param action: 操作类型，1 表示添加 kext，2 表示删除 kext，3 表示禁用 kext，4 表示启用 kext
    :param kextname: kext 的名称（不包含扩展名）
    :param status: 状态，1 表示启用，2 表示禁用
    :param plist_file: plist 文件路径
    """
    # 确保 temp 目录存在
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 找到 Kernel 下的 Add 键
    kernel_add = plist_data.get('Kernel', {}).get('Add', [])

    # 根据 action 执行操作
    if action == 1:
        # 添加并启用 kext
        kext_path = f"{kextname}.kext"
        new_kext = {
            'Arch': 'Any',
            'BundlePath': kext_path,
            'Comment': f'Custom kernel extension {kextname}',
            'Enabled': True,
            'ExecutablePath': f"Contents/MacOS/{kextname}",
            'MaxKernel': '',
            'MinKernel': '10.0.0',
            'PlistPath': f"Contents/Info.plist"
        }
        kernel_add.append(new_kext)
        print(f"Added and enabled {kextname}")
    elif action == 2:
        # 删除 kext
        kext_path = f"{kextname}.kext"
        kernel_add = [item for item in kernel_add if item.get('BundlePath') != kext_path]
        print(f"Removed {kextname}")
    elif action == 3:
        # 禁用 kext
        kext_path = f"{kextname}.kext"
        for item in kernel_add:
            if item.get('BundlePath') == kext_path:
                item['Enabled'] = False
                print(f"Disabled {kextname}")
                break
    elif action == 4:
        # 启用 kext
        kext_path = f"{kextname}.kext"
        for item in kernel_add:
            if item.get('BundlePath') == kext_path:
                item['Enabled'] = True
                print(f"Enabled {kextname}")
                break

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        plist_data['Kernel']['Add'] = kernel_add
        plistlib.dump(plist_data, f, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description="Edit Kernel Add in a plist file.")
    parser.add_argument("action", type=int, choices=[1, 2, 3, 4], help="Action: 1 to add and enable, 2 to remove, 3 to disable, 4 to enable")
    parser.add_argument("kextname", type=str, help="The name of the kext")
    parser.add_argument("status", type=int, choices=[1, 2], help="Status: 1 to enable, 2 to disable (only for adding)")

    args = parser.parse_args()

    try:
        edit_kernel_add(args.action, args.kextname, args.status)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()