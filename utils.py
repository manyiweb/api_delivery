import yaml
import os


# 读取数据
def load_yaml_data(file_path):
    """从 YAML 文件中加载原始配置数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: YAML file not found at {file_path}")
        return None


# 获取数据文件路径
def get_data_file_path(filename):
    """获取 data 目录下的文件路径"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_root, 'data', filename)


