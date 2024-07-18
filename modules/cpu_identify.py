# cpu_identify.py
# powered by laobamac,请遵循GPLv3开源协议
import cpuinfo
import re

def identify_cpu():
    # 获取 CPU 信息
    info = cpuinfo.get_cpu_info()
    
    # 获取 CPU 型号
    cpu_model = info.get('brand_raw', 'Unknown')
    
    # 检查 CPU 厂商
    if "Intel" in cpu_model:
        return identify_intel_cpu(cpu_model)
    elif "AMD" in cpu_model:
        return identify_amd_cpu(cpu_model)
    else:
        return "Unknown", "Unknown", cpu_model, "Unknown"

def identify_intel_cpu(cpu_model):
    # 尝试匹配 Intel CPU 代数
    match = re.search(r"Intel$$R$$ Core(TM) i\d+-(\d+)", cpu_model)
    if match:
        generation = int(match.group(1))
    else:
        generation = "Unknown"
    
    # 检查是否有核显
    has_gpu = "F" not in cpu_model and "KF" not in cpu_model
    
    return "Intel", generation, cpu_model, has_gpu

def identify_amd_cpu(cpu_model):
    # 尝试匹配 AMD Ryzen 系列
    match = re.search(r"AMD Ryzen (?:R\d+)", cpu_model)
    if match:
        series = match.group(1)
        series_number = int(re.search(r"\d+", series).group())
    else:
        series_number = "Unknown"
    
    # 检查是否有核显
    has_gpu = "G" in cpu_model
    
    return "AMD", series_number, cpu_model, has_gpu

def main():
    vendor, generation, model, gpu = identify_cpu()
    print(f"CPU Vendor: {vendor}")
    print(f"Generation: {generation}")
    print(f"Model: {model}")
    print(f"Integrated GPU: {'Yes' if gpu else 'No'}")

if __name__ == "__main__":
    main()
