"""
创建图书
Create book

"""
# encoding = utf-8
# python 3.13.5

from loguru import logger
from backend.utils.path import create_dir, get_book_path

async def create_book(book_id: str, book_name: str, user_uid: str) -> bool:
    """
    创建图书
    Create book
    Args:
        book_id (str): 图书 ID Book ID
        book_name (str): 图书名称 Book name
        user_uid (str): 用户 UID User UID
    Returns:
        bool: 创建成功返回 True, 失败返回 False True if creation succeeded, False otherwise
    """
    book_path = get_book_path(book_id)
    from backend.utils.json import json_dump
    from backend.utils.user import get_user_info
    
    user_info = await get_user_info(user_uid)
    if not user_info:
        logger.error(f"用户 {user_uid} 不存在")
        return False
    
    if await create_dir(book_path):
        # 创建书籍元数据
        metadata = {
            'book_id': book_id,
            'name': book_name,
            'owner_uid': user_uid,
            'owner_name': user_info['name'],
            'created_at': str(user_info['created_at'])
        }
        json_dump(f"{book_path}/info.json", metadata)
        logger.info(f"创建图书 {book_name} 成功, 所有者: {user_info['name']}")
        return True
    logger.error(f"创建图书目录 {book_id} 失败")
    return False