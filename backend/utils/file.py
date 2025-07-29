"""
文件工具类
File utilities

"""
# encoding = utf-8
# python 3.13.5

import pathlib
from loguru import logger

async def delete_file(file_path: str) -> bool:
    """
    删除文件
    Delete file
    Args:
        file_path (str): 文件路径 File path
    Returns:
        bool: 删除成功返回 True, 失败返回 False True if deletion succeeded, False otherwise
    """
    try:
        pathlib.Path(file_path).unlink()
        return True
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在")
        return False
    except PermissionError:
        logger.error(f"文件 {file_path} 权限错误")
        return False
    except Exception as e:
        logger.error(f"文件 {file_path} 删除失败, 异常信息: {e}")
        return False


async def write_file(file_path: str, data: bytes) -> bool:
    """
    写入文件
    Write file
    Args:
        file_path (str): 文件路径 File path
        data (bytes): 文件数据 File data
    Returns:
        bool: 写入成功返回 True, 失败返回 False True if write succeeded, False otherwise
    """
    try:
        with open(file_path, "wb") as f:
            f.write(data)
        return True
    except IOError:
        logger.error(f"文件 {file_path} 写入失败")
        return False
    except Exception as e:
        logger.error(f"文件 {file_path} 写入失败, 异常信息: {e}")
        return False

async def get_file_content(file_path: str) -> bytes:
    """
    获取文件内容
    Get file content
    Args:
        file_path (str): 文件路径 File path
    Returns:
        bytes: 文件内容 File content
    """
    """
    读取文件
    Args:
        file_path: 文件路径
    Returns:
        文件数据
    """
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except IOError:
        logger.error(f"文件 {file_path} 读取失败")
        return b""
    except Exception as e:
        logger.error(f"文件 {file_path} 读取失败, 异常信息: {e}")
        return b""

async def get_file_size(file_path: str) -> int:
    """
    获取文件大小
    Args:
        file_path: 文件路径
    Returns:
        文件大小
    """
    try:
        return pathlib.Path(file_path).stat().st_size
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在")
        return 0
    except Exception as e:
        logger.error(f"文件 {file_path} 获取大小失败, 异常信息: {e}")
        return 0

async def rename_file(file_path: str, new_file_path: str) -> bool:
    """
    重命名文件
    Args:
        file_path: 文件路径
        new_file_path: 新文件路径
    Returns:
        重命名成功返回 True, 失败返回 False
    """
    try:
        pathlib.Path(file_path).rename(new_file_path)
        return True
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在")
        return False
    except PermissionError:
        logger.error(f"文件 {file_path} 权限错误")
        return False
    except Exception as e:
        logger.error(f"文件 {file_path} 重命名失败, 异常信息: {e}")
        return False

async def copy_file(file_path: str, new_file_path: str) -> bool:
    """
    复制文件
    Args:
        file_path: 文件路径
        new_file_path: 新文件路径
    Returns:
        复制成功返回 True, 失败返回 False
    """
    try:
        pathlib.Path(file_path).copy(new_file_path)
        return True
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在")
        return False
    except PermissionError:
        logger.error(f"文件 {file_path} 权限错误")
        return False
    except Exception as e:
        logger.error(f"文件 {file_path} 复制失败, 异常信息: {e}")
        return False

async def create_file(file_path: str) -> bool:
    """
    创建文件
    Args:
        file_path: 文件路径
    Returns:
        创建成功返回 True, 失败返回 False
    """
    try:
        pathlib.Path(file_path).touch()
        return True
    except Exception as e:
        logger.error(f"文件 {file_path} 创建失败, 异常信息: {e}")
        return False
