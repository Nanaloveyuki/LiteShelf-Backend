"""
路径工具类
"""

import pathlib

def get_absolute_path(path: str) -> str:
    """
    获取绝对路径
    Args:
        path: 路径
    Returns:
        绝对路径
    """
    return str(pathlib.Path(path).absolute())

def get_file_name(path: str) -> str:
    """
    获取文件名
    Args:
        path: 路径
    Returns:
        文件名
    """
    return pathlib.Path(path).name

def get_file_extension(path: str) -> str:
    """
    获取文件扩展名
    Args:
        path: 路径
    Returns:
        文件扩展名
    """
    return pathlib.Path(path).suffix

def get_file_parent_path(path: str) -> str:
    """
    获取文件父路径
    Args:
        path: 路径
    Returns:
        文件父路径
    """
    return str(pathlib.Path(path).parent)

def get_book_path(book_id: str) -> str:
    """
    获取图书路径
    Args:
        book_id: 图书 ID
    Returns:
        图书路径
    """
    return str(pathlib.Path(__file__).parent.parent / "books" / book_id).parent

def create_dir(path: str) -> bool:
    """
    创建目录
    Args:
        path: 目录路径
    Returns:
        创建成功返回 True, 失败返回 False
    """
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"目录 {path} 创建失败, 异常信息: {e}")
        return False

def delete_dir(path: str) -> bool:
    """
    删除目录
    Delete directory
    Args:
        path (str): 目录路径 Directory path
    Returns:
        bool: 删除成功返回 True, 失败返回 False True if deletion succeeded, False otherwise
    """
    try:
        pathlib.Path(path).rmdir()
        return True
    except Exception as e:
        logger.error(f"目录 {path} 删除失败, 异常信息: {e}")
        return False

def get_books_dir() -> str:
    """
    获取书籍存储目录
    Get books storage directory
    Returns:
        str: 书籍目录路径 Books directory path
    """
    return str(pathlib.Path(__file__).parent.parent / "books")

def get_user_path(user_uid: str) -> str:
    """
    获取用户路径
    Get user path
    Args:
        user_uid (str): 用户 UID User UID   
    Returns:
        str: 用户路径 User path
    """
    return str(pathlib.Path(__file__).parent.parent / "users" / f"{user_uid}.json")
