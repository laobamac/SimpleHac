# install_dependencies.py
import subprocess

def install(package):
    subprocess.check_call([package])

if __name__ == "__main__":
    # 列出所有需要安装的依赖
    dependencies = ['tqdm', 'cpuinfo']

    # 使用 pip 安装依赖
    for package in dependencies:
        install('pip3 install {}'.format(package))
