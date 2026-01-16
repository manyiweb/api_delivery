import os

import yaml

from utils.logger import logger


def load_yaml_data(file_path):
    """Load YAML data from a file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"YAML file not found: {file_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"YAML parse error: {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to load YAML: {file_path}: {e}")
        return None


# def get_data_file_path(filename):
#     """Return the absolute path for a data file under /data."""
#     project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(project_root, 'data', filename)

# ... existing code ...
def get_data_file_path(filename):
    """获取 data 目录下的文件路径，支持环境自动切换"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 获取当前环境
    env = os.getenv("ENV", "test")

    # 如果是 uat 环境，优先查找带 _uat 后缀的文件
    if env == "uat":
        name_parts = filename.rsplit('.', 1)
        uat_filename = f"{name_parts[0]}_uat.{name_parts[1]}"
        uat_path = os.path.join(project_root, 'data', uat_filename)

        # 如果 uat 特有的文件存在则返回，否则使用默认文件
        if os.path.exists(uat_path):
            return uat_path

    return os.path.join(project_root, 'data', filename)
# ... existing code ...

if __name__ == '__main__':
    print(get_data_file_path('delivery_data.yaml'))
