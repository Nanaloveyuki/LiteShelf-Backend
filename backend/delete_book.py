"""
删除图书
Delete book

"""
# encoding = utf-8
# python 3.13.5

from loguru import logger
from backend.utils.path import delete_dir, get_book_path
from backend.utils import check_pswd

async def delete_book(
        book_id: str,
        book_name: str,
        user_name: str,
        user_uid: str,
        user_pswd: str,
    ) -> bool:
    """
    删除图书
    Delete book
    Args:
        book_id (str): 图书 ID Book ID
        book_name (str): 图书名称 Book name
        user_name (str): 用户名称 User name
        user_uid (str): 用户 UID User UID
        user_pswd (str): 用户密码 User password
    Returns:
        bool: 删除成功返回 True, 失败返回 False True if deletion succeeded, False otherwise
    """
    if not await check_pswd(user_uid, user_pswd):
        logger.info(f"用户 {user_name} 因为密码错误, 删除失败")
        return False
    
    try:
        book_path = get_book_path(book_id)
        await delete_dir(book_path)
    except Exception as e:
        logger.error(f"删除图书目录 {book_id} 失败, 异常信息: {e}")
        return False
    return True