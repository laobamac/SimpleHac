import os
import shutil
import zipfile
import requests
from tqdm import tqdm
# powered by laobamac,请遵循GPLv3开源协议
def ensure_target_folder_exists(target_path):
    """确保目标文件夹存在，如果不存在则创建"""
    if not os.path.exists(target_path):
        os.makedirs(target_path)

def download_file(url, folder_path, filename):
    """下载文件并显示进度条"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(os.path.join(folder_path, filename), "wb") as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    else:
        print(f"Failed to download {filename}")

def extract_and_copy_kext(zip_path, extract_path, kext_name):
    """解压zip文件并将kext文件夹复制到指定位置"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    kext_path = os.path.join(extract_path, kext_name)
    target_path = os.path.join(extract_path, '..', 'Kexts', kext_name)
    shutil.copytree(kext_path, target_path)
    os.remove(zip_path)

def download_kexts_and_ssdts(kexts, ssdts, download_path):
    """下载Kexts和SSDTs"""
    failed_downloads = []
    for kext in kexts:
        url = f"http://api.simplehac.cn/v1/dl/kext/{kext}.zip"
        download_file(url, os.path.join(download_path, 'Kexts'), f"{kext}.zip")
        extract_path = os.path.join(download_path, 'Kexts', kext)
        ensure_target_folder_exists(extract_path)
        extract_and_copy_kext(os.path.join(download_path, 'Kexts', f"{kext}.zip"), extract_path, kext)
    for ssdt in ssdts:
        url = f"http://api.simplehac.cn/v1/dl/ssdt/{ssdt}"
        download_file(url, os.path.join(download_path, 'ACPI'), ssdt)

def main(oc_version, cpu_vendor=None, generation=None, igpu=None, cores=None):
    # 如果用户没有指定CPU信息，使用identify_cpu获取
    if not (cpu_vendor and cores):
        from cpu_identify import identify_cpu
        cpu_vendor, generation, _, gpu, core_count = identify_cpu()
        cores = core_count

    # 确定资源文件夹路径
    resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources')

    # 确定目标EFI文件夹路径
    temp_efi_path = os.path.join(resources_path, '..', 'temp', 'EFI')
    ensure_target_folder_exists(temp_efi_path)

    # 确定OC文件夹路径
    oc_folder = os.path.join(temp_efi_path, 'OC')
    ensure_target_folder_exists(oc_folder)

    # 确定BOOT文件夹路径
    boot_folder = os.path.join(temp_efi_path, 'BOOT')
    ensure_target_folder_exists(boot_folder)

    # 复制config.plist文件
    copy_config_plist(resources_path, oc_folder, cpu_vendor, cores)

    # 复制OpenCore文件
    copy_opencore_files(resources_path, oc_version, oc_folder, boot_folder)

    # 发送请求获取INI文件
    params = {
        'vendor': cpu_vendor,
        'generation': generation,
        'cores': str(cores),
        'igpu': igpu
    }
    response = requests.get("http://api.simplehac.cn/v1/", params=params)
    if response.status_code == 200:
        ini_content = response.text
        ini_filename = "ini_loader.ini"
        with open(os.path.join(temp_efi_path, ini_filename), "w") as ini_file:
            ini_file.write(ini_content)
        print(f"INI file saved as {ini_filename}")

        # 解析INI文件并下载Kexts和SSDTs
        # 这里需要根据实际INI文件内容进行解析
        kexts = [line.split('=')[0] for line in ini_content.splitlines() if line.startswith('Add')]
        ssdts = [line.split('=')[0] for line in ini_content.splitlines() if line.startswith('SSDT')]
        download_path = os.path.join(temp_efi_path, 'EFI', 'OC')
        download_kexts_and_ssdts(kexts, ssdts, download_path)

        # 运行ini_loader.py脚本
        ini_loader_path = os.path.join(temp_efi_path, ini_filename)
        run_ini_loader(ini_loader_path)

        # 下载res.zip
        oc_zip_url = f"http://api.simplehac.cn/v1/dl/resources/{oc_version}"
        download_file(oc_zip_url, temp_efi_path, f"res_{oc_version}.zip")

        # 解压res.zip
        with zipfile.ZipFile(os.path.join(temp_efi_path, f"res_{oc_version}.zip"), 'r') as zip_ref:
            zip_ref.extractall(oc_folder)

        print("ACE All Done! Have fun!")
        time.sleep(3)  # 等待3秒

        # 清理temp目录
        for item in os.listdir('temp'):
            item_path = os.path.join('temp', item)
            if item != 'EFI' and os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif item != 'EFI' and os.path.isfile(item_path):
                os.remove(item_path)

        print("Remaining temp files cleaned up.")
    else:
        print("Failed to fetch INI file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto create EFI for Hackintosh.")
    parser.add_argument("oc_version", type=str, help="OpenCore version (e.g., 1.0.0, latest)")
    parser.add_argument("--vendor", type=str, help="CPU vendor (AMD or Intel)")
    parser.add_argument("--generation", type=str, help="CPU generation")
    parser.add_argument("--igpu", type=str, choices=['Yes', 'No'], help="Integrated GPU presence")
    parser.add_argument("--cores", type=int, help="Number of CPU cores")
    args = parser.parse_args()

    main(args.oc_version, args.vendor, args.generation, args.igpu, args.cores)
