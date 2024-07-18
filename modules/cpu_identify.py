import cpuinfo
import re
# powered by laobamac,请遵循GPLv3开源协议
def identify_cpu():
    # 获取 CPU 信息
    info = cpuinfo.get_cpu_info()

    # 获取 CPU 型号
    cpu_model = info.get('brand_raw', 'Unknown')

    # 获取 CPU 核心数量
    core_count = info.get('core_count', 'Unknown')

    # 检查 CPU 厂商
    if "Intel" in cpu_model:
        return identify_intel_cpu(cpu_model, core_count)
    elif "AMD" in cpu_model:
        return identify_amd_cpu(cpu_model, core_count)
    else:
        return "Unknown", "Unknown", cpu_model, "Unknown", core_count

def identify_intel_cpu(cpu_model, core_count):
    # 尝试匹配 Intel CPU 代数
    match = re.search(r"Intel$$R$$ Core(TM) i\d+-(\d+)", cpu_model)
    if match:
        generation = int(match.group(1))
    else:
        generation = "Unknown"

    # 检查是否有核显
    has_gpu = "F" not in cpu_model and "KF" not in cpu_model

    return "Intel", generation, cpu_model, has_gpu, core_count

def identify_amd_cpu(cpu_model, core_count):
    # 尝试匹配 AMD Ryzen 系列
    match = re.search(r"AMD Ryzen (?:R\d+)", cpu_model)
    if match:
        series = match.group(1)
        # 提取系列号，假设系列号是型号中的第一个数字
        series_number = int(re.search(r"(\d+)00", cpu_model).group(1)) * 1000
    else:
        series_number = "Unknown"

    # 检查是否有核显
    has_gpu = "G" in cpu_model

    return "AMD", series_number, cpu_model, has_gpu, core_count

def main():
    vendor, generation, model, gpu, core_count = identify_cpu()
    print(f"CPU Vendor: {vendor}")
    print(f"Generation: {generation}")
    print(f"Model: {model}")
    print(f"Integrated GPU: {'Yes' if gpu else 'No'}")
    print(f"Core Count: {core_count}")

if __name__ == "__main__":
    main()
