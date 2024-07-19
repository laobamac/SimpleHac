import os
import shutil
import argparse
from cpu_identify import identify_cpu
# powered by laobamac,请遵循GPLv3开源协议
def ensure_target_folder_exists(target_path):
    """确保目标文件夹存在，如果不存在则创建"""
    if not os.path.exists(target_path):
        os.makedirs(target_path)

def copy_config_plist(resources_path, oc_folder, cpu_vendor, generation, igpu, cores):
    """根据CPU类型和代数复制相应的config.plist文件"""
    # 确定目标config.plist路径
    config_folder = os.path.join(resources_path, cpu_vendor.lower(), generation)
    
    # 复制config.plist
    config_plist_path = os.path.join(config_folder, 'config.plist')
    if os.path.exists(config_plist_path):
        shutil.copy(config_plist_path, oc_folder)
        print(f"config.plist for {cpu_vendor} {generation} with iGPU={igpu} and Cores={cores} copied to {oc_folder}")
    else:
        print("config.plist not found.")

def copy_opencore_files(resources_path, oc_version, target_oc_path, target_boot_path):
    """从resources文件夹中的OpenCore复制文件"""
    opencore_path = os.path.join(resources_path, 'OpenCore')
    opencore_version_path = os.path.join(opencore_path, oc_version)
    
    # 复制bootx64.efi和opencore.efi
    for filename in ['bootx64.efi', 'opencore.efi']:
        src_file_path = os.path.join(opencore_version_path, filename)
        dst_file_path = os.path.join(target_oc_path, filename)
        if os.path.exists(src_file_path):
            shutil.copy(src_file_path, dst_file_path)
            print(f"{filename} copied to {target_oc_path}")
        else:
            print(f"{filename} not found in OpenCore version {oc_version}.")

def main(oc_version, cpu_vendor=None, generation=None, igpu=None, cores=None):
    # 如果用户没有指定CPU信息，使用identify_cpu获取
    if not (cpu_vendor and generation and igpu and cores):
        cpu_vendor, generation, _, gpu, cores = identify_cpu()
        igpu = 'Yes' if gpu else 'No'

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
    copy_config_plist(resources_path, oc_folder, cpu_vendor, generation, igpu, cores)
    
    # 复制OpenCore文件
    copy_opencore_files(resources_path, oc_version, oc_folder, boot_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto create EFI for Hackintosh.")
    parser.add_argument("oc_version", type=str, help="OpenCore version (e.g., 0.8.9, 1.0.0, latest)")
    parser.add_argument("--vendor", type=str, help="CPU vendor (AMD or Intel)")
    parser.add_argument("--generation", type=str, help="CPU generation")
    parser.add_argument("--igpu", type=str, choices=['Yes', 'No'], help="Integrated GPU presence")
    parser.add_argument("--cores", type=int, help="Number of CPU cores")
    args = parser.parse_args()

    main(args.oc_version, args.vendor, args.generation, args.igpu, args.cores)
