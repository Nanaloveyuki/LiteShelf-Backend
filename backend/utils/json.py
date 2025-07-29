"""
JSON 工具类
JSON utilities

"""
# encoding = utf-8
# python 3.13.5

import json
from loguru import logger

def json_load(file_path: str) -> dict:
    """
    从文件加载 JSON 数据
    Load JSON data from file
    Args:
        file_path (str): JSON 文件路径 JSON file path
    Returns:
        dict: JSON 数据 JSON data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在")
        return {}
    except json.JSONDecodeError:
        logger.error(f"文件 {file_path} 格式错误")
        return {}
    except Exception as e:
        logger.error(f"加载 JSON 文件 {file_path} 失败, 异常信息: {e}")
        return {}

def json_dump(file_path: str, data: dict) -> None:
    """
    将 JSON 数据写入文件
    Write JSON data to file
    Args:
        file_path (str): JSON 文件路径 JSON file path
        data (dict): JSON 数据 JSON data
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        logger.error(f"文件 {file_path} 写入失败")
    except json.JSONDecodeError:
        logger.error(f"文件 {file_path} 格式错误")
    except Exception as e:
        logger.error(f"文件 {file_path} 写入失败, 异常信息: {e}")
