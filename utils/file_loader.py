import os

import yaml
from dotenv import load_dotenv

from utils.logger import logger


def load_yaml_data(file_path):
    """从文件路径加载 YAML 数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"YAML 文件不存在: {file_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"YAML 解析错误: {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"加载 YAML 失败: {file_path}: {e}")
        return None


# ... 现有代码 ...
def get_data_file_path(filename):
    """获取 data 目录下的文件路径，支持环境自动切换"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 获取当前环境
    env = os.getenv("ENV")

    # 如果是 uat 环境，优先查找带 _uat 后缀的文件
    if env == "uat":
        name_parts = filename.rsplit('.', 1)
        uat_filename = f"{name_parts[0]}_uat.{name_parts[1]}"
        uat_path = os.path.join(project_root, 'data', uat_filename)

        # 如果 uat 特有的文件存在则返回，否则使用默认文件
        if os.path.exists(uat_path):
            return uat_path

    return os.path.join(project_root, 'data', filename)

if __name__ == '__main__':
    load_dotenv()
    if os.getenv("ENV") == "uat":
        raw_data = get_data_file_path("mt_delivery_data_uat.yaml")
        print(raw_data)
    else:
        raw_data = get_data_file_path("mt_delivery_data.yaml")
        print(raw_data)
