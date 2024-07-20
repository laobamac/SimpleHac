# install_dependencies.py
import subprocess

def install(package):
    subprocess.check_call([package])

if __name__ == "__main__":
    # 列出所有需要安装的依赖
    dependencies = ['tqdm', 'cpuinfo', 'shutil', 'requests', 'psutil', 'gpuinfo', 'zipfile', 'os']

    # 使用 pip 安装依赖
    for package in dependencies:
        install('pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple {}'.format(package))
