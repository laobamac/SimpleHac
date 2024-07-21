import subprocess
import requests
# powered by laobamac，请遵循GPLv3开源协议
def get_hardware_info(type, property_name):
    """
    使用WMIC命令获取Windows系统的硬件信息。
    :param type: 'videocontroller' 或 'diskdrive'，分别获取显卡和硬盘信息。
    :param property_name: WMIC查询的属性名称。
    """
    command = f'wmic path Win32_{type} get {property_name}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        # 排除包含"Name"或"Mirage Driver"的行
        return [line.strip() for line in result.stdout.split('\n') if line.strip() and "Name" not in line and "Mirage Driver" not in line]
    else:
        print(f"Failed to get {type} information: {result.stderr}")
        return []

def fetch_hardware_list(hw_type):
    """
    从API获取硬件列表。
    :param hw_type: 'sgpu', 'dgpu', 'disk'，分别对应支持的显卡列表、存疑的显卡型号列表和不支持的硬盘型号列表。
    """
    url = f"http://api.simplehac.cn/hw.php?hw={hw_type}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return [item.strip().lower() for item in response.text.split('\n') if item]
    except requests.RequestException as e:
        print(f"Failed to fetch {hw_type} list: {e}")
        return []

def mark_hardware(hardware_list, supported_list, doubted_list, unsupport_list, hardware_type):
    """
    根据硬件型号和列表标记硬件。
    """
    for hardware in hardware_list:
        if "Name" in hardware or "Mirage Driver" in hardware:
            continue  # 跳过包含特定字符串的硬件
        hardware_lower = hardware.lower()
        # 检查显卡是否在支持列表或存疑列表中
        if hardware_type == 'gpu':
            if any(supported in hardware_lower for supported in supported_list):
                print(f"[Supported] {hardware}")
            elif any(doubted in hardware_lower for doubted in doubted_list):
                print(f"[Doubted] {hardware}")
            else:
                print(f"[Unsupported] {hardware}")
        # 检查硬盘是否在不支持列表中
        elif hardware_type == 'disk':
            if any(unsupport in hardware_lower for unsupport in unsupport_list):
                print(f"[Unsupported] {hardware}")
            else:
                print(f"[Supported] {hardware}")

def main():
    # 获取显卡信息
    gpus = get_hardware_info('videocontroller', 'Name')

    # 获取硬盘型号信息
    disks = get_hardware_info('diskdrive', 'Model')

    # 获取硬件列表
    sgpu_list = fetch_hardware_list('sgpu')
    dgpu_list = fetch_hardware_list('dgpu')
    unsupport_disk_list = fetch_hardware_list('disk')

    # 根据列表标记显卡
    mark_hardware(gpus, sgpu_list, dgpu_list, [], 'gpu')

    # 根据列表标记硬盘
    mark_hardware(disks, [], [], unsupport_disk_list, 'disk')

if __name__ == "__main__":
    main()
