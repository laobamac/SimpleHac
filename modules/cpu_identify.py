# cpu_identify.py
# powered by laobamac,请遵循GPLv3开源协议
import platform
import re

def identify_cpu():
    cpu_info = platform.processor()
    if "Intel" in cpu_info:
        return identify_intel_cpu()
    elif "AMD" in cpu_info:
        return identify_amd_cpu()
    else:
        return "Unknown", "Unknown", "Unknown", "Unknown"

def identify_intel_cpu():
    model = platform.platform().split()[-1]
    
    # 尝试匹配 Intel Core 系列
    match = re.search(r"Intel$$R$$ Core(TM) i\d+-(\d+)", model)
    if match:
        generation = int(match.group(1))
        return "Intel", generation, model, has_integrated_gpu(model)
    
    return "Intel", "Unknown", model, has_integrated_gpu(model)

def identify_amd_cpu():
    model = platform.platform().split()[-1]
    
    # 尝试匹配 AMD Ryzen 系列
    match = re.search(r"AMD Ryzen (?:R\d+)", model)
    if match:
        series = match.group(1)
        series_number = int(re.search(r"\d+", series).group())
        return "AMD", series_number, model, has_integrated_gpu(model)
    
    return "AMD", "Unknown", model, has_integrated_gpu(model)

def has_integrated_gpu(model):
    # 检查 Intel CPU 是否有集成显卡（型号中不包含 "F" 和 "KF"）
    if "Intel" in model:
        return not ("F" in model or "KF" in model)
    
    # 检查 AMD CPU 是否有集成显卡（型号中包含 "G"）
    return "G" in model

def main():
    vendor, generation, model, gpu = identify_cpu()
    print(f"CPU Vendor: {vendor}")
    print(f"Generation: {generation}")
    print(f"Model: {model}")
    print(f"Integrated GPU: {'Yes' if gpu else 'No'}")

if __name__ == "__main__":
    main()