""""
用户管理工具
User management utilities

"""
# encoding = utf-8
# python 3.13.5

import uuid
from loguru import logger
from backend.utils.json import json_dump, json_load
from backend.utils.path import get_user_path, create_dir
from backend.utils.pswd import check_pswd

import datetime
import bcrypt
from pathlib import Path

# 确保用户名唯一
def _is_username_unique(user_name: str) -> bool:
    users_dir = Path(get_user_path('')).parent
    if not users_dir.exists():
        return True
    for file in users_dir.glob('*.json'):
        try:
            user_info = json_load(str(file))
            if user_info.get('user_name') == user_name:
                return False
        except Exception as e:
            logger.warning(f"检查用户名唯一性时出错: {e}")
    return True
def create_user(user_name: str, user_pswd: str) -> str:
    """
    创建新用户
    Create new user
    Args:
        user_name (str): 用户名 User name
        user_pswd (str): 用户密码 User password
    Returns:
        str: 用户 UID User UID
    """
    if not _is_username_unique(user_name):
        logger.error(f"用户名已存在: {user_name}")
        raise ValueError("Username already exists")

    user_uid = str(uuid.uuid4())
    user_path = get_user_path(user_uid)
    
    # 确保用户目录存在
    create_dir(get_user_path(user_uid).rsplit('/', 1)[0])
    
    # 密码哈希处理
    salt = bcrypt.gensalt()
    hashed_pswd = bcrypt.hashpw(user_pswd.encode('utf-8'), salt).decode('utf-8')
    
    user_data = {
        'user_uid': user_uid,
        'user_name': user_name,
        'pswd': hashed_pswd,
        'created_at': str(datetime.datetime.now()),
        'avatar_url': '',  # 用户头像URL User avatar URL
        'bio': ''  # 用户简介 User biography
    }
    
    try:
        json_dump(user_path, user_data)
        logger.info(f"用户 {user_name} 创建成功, UID: {user_uid}")
        return user_uid
    except Exception as e:
        logger.error(f"用户创建失败: {e}")
        raise
def get_user_info(user_uid: str) -> dict:
    """
    获取用户信息
    Get user information
    Args:
        user_uid (str): 用户 UID
    Returns:
        dict: 用户信息 User information
    """
    user_path = get_user_path(user_uid)
    try:
        return json_load(user_path)
    except FileNotFoundError:
        logger.error(f"用户不存在: {user_uid}")
        raise
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        raise

def update_user_profile(user_uid: str, **kwargs) -> bool:
    """
    更新用户资料
    Update user profile
    Args:
        user_uid (str): 用户UID
        **kwargs: 可选字段 Optional fields: avatar_url, bio
    Returns:
        bool: 更新是否成功
    ""
    try:
        user_info = get_user_info(user_uid)
        # 更新提供的字段 Update provided fields
        if 'avatar_url' in kwargs:
            user_info['avatar_url'] = kwargs['avatar_url']
        if 'bio' in kwargs:
            user_info['bio'] = kwargs['bio']
        user_info['updated_at'] = str(datetime.datetime.now())
        
        json_dump(get_user_path(user_uid), user_info)
        logger.info(f"用户资料更新成功: {user_uid}")
        return True
    except Exception as e:
        logger.error(f"用户资料更新失败: {e}")
        return False

def update_user_pswd(user_uid: str, old_pswd: str, new_pswd: str) -> bool:
    """
    更新用户密码
    Update user password
    Args:
        user_uid (str): 用户 UID
        old_pswd (str): 旧密码 Old password
        new_pswd (str): 新密码 New password
    Returns:
        bool: 更新成功返回 True, 失败返回 False
    """
    try:
        if not check_pswd(user_uid, old_pswd):
            logger.error(f"用户 {user_uid} 密码更新失败, 旧密码错误")
            return False
        
        user_info = get_user_info(user_uid)
        # 密码哈希处理
        salt = bcrypt.gensalt()
        hashed_new_pswd = bcrypt.hashpw(new_pswd.encode('utf-8'), salt).decode('utf-8')
        user_info['pswd'] = hashed_new_pswd
        user_info['updated_at'] = str(datetime.datetime.now())
        
        json_dump(get_user_path(user_uid), user_info)
        logger.info(f"用户 {user_uid} 密码更新成功")
        return True
    except Exception as e:
        logger.error(f"用户密码更新失败: {e}")
        return False