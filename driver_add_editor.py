# driver_add_editor.py
# powered by laobamac,请遵循GPLv3开源协议
import plistlib
import argparse
import os

def edit_driver_add(drvname, status, plist_file='temp/config.plist'):
    """
    编辑 UEFI 中的 Drivers。

    :param drvname: 驱动的名称
    :param status: 状态，1 表示启用，2 表示禁用
    :param plist_file: plist 文件路径
    """
    # 确保 temp 目录存在
    if not os.path.exists('temp'):
        os.makedirs('temp')

    # 读取 plist 文件
    with open(plist_file, 'rb') as f:
        plist_data = plistlib.load(f)

    # 找到 UEFI 下的 Drivers 键
    uefi_data = plist_data.get('UEFI', {})
    drivers_data = uefi_data.get('Drivers', [])

    # 查找驱动
    driver_found = False
    for driver in drivers_data:
        if driver.get('Path') and drvname in driver.get('Path'):
            driver['Enabled'] = (status == 1)
            driver_found = True
            break

    if not driver_found:
        print(f"Error: Driver '{drvname}' not found in UEFI Drivers.")
        return

    # 保存修改后的 plist 文件
    with open(plist_file, 'wb') as f:
        uefi_data['Drivers'] = drivers_data
        plist_data['UEFI'] = uefi_data
        plistlib.dump(plist_data, f, sort_keys=False)
    print(f"Driver '{drvname}' has been {'enabled' if status == 1 else 'disabled'}.")

def main():
    parser = argparse.ArgumentParser(description="Edit Drivers in UEFI in a plist file.")
    parser.add_argument("drvname", type=str, help="The name of the driver")
    parser.add_argument("status", type=int, choices=[1, 2], help="Status: 1 to enable, 2 to disable")

    args = parser.parse_args()

    try:
        edit_driver_add(args.drvname, args.status)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
