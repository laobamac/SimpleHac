# cpu_identify.py

import cpuinfo
import re

def identify_cpu():
    # 获取 CPU 信息
    info = cpuinfo.get_cpu_info()
    
    # 获取 CPU 型号
    cpu_model = info.get('brand', 'Unknown')
    
    # 检查 CPU 厂商
    if "Intel" in cpu_model:
        return identify_intel_cpu(cpu_model)
    elif "AMD" in cpu_model:
        return identify_amd_cpu(cpu_model)
    else:
        return "Unknown", "Unknown", cpu_model, "Unknown"

def identify_intel_cpu(cpu_model):
    # 英特尔处理器的代数通常不在型号中明确表示，因此这里返回 "Unknown"
    generation = "Unknown"
    # 检查是否有核显
    has_gpu = "F" not in cpu_model and "KF" not in cpu_model
    return "Intel", generation, cpu_model, has_gpu

def identify_amd_cpu(cpu_model):
    # 尝试匹配 AMD Ryzen 系列和代数
    match = re.search(r"AMD Ryzen (\d+)", cpu_model)
    if match:
        series = int(match.group(1))
    else:
        series = "Unknown"
    
    # 检查是否有核显
    has_gpu = "G" in cpu_model or "GE" in cpu_model
    
    return "AMD", series, cpu_model, not has_gpu

def main():
    vendor, generation, model, gpu = identify_cpu()
    print(f"CPU Vendor: {vendor}")
    print(f"Generation: {generation}")
    print(f"Model: {model}")
    print(f"Integrated GPU: {'Yes' if gpu else 'No'}")

if __name__ == "__main__":
    main()
