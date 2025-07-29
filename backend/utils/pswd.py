"""
检查用户密码是否正确
Check user password

"""
# encoding = utf-8
# python 3.13.5

from backend.utils.json import json_load
from backend.utils.path import get_user_path

async def check_pswd(user_uid: str, user_pswd: str) -> bool:
    """
    检查用户密码是否正确
    Check user password
    Args:
        user_uid (str): 用户 UID User UID
        user_pswd (str): 用户密码 User password
    Returns:
        bool: True: 密码正确 Password correct, False: 密码错误 Password incorrect
    """
    user_path = get_user_path(user_uid)
    user_info = json_load(user_path)
    if user_info["pswd"] == user_pswd:
        return True
    return False
