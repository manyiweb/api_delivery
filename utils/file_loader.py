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


def get_data_file_path(filename):
    """Return the absolute path for a data file under /data."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, 'data', filename)


if __name__ == '__main__':
    print(get_data_file_path('delivery_data.yaml'))
