"""
UUID生成工具
UUID generation utilities

"""
# encoding = utf-8
# python 3.13.5

import uuid

def generate_uuid() -> str:
    """
    生成UUID
    Generate UUID
    Returns:
        str: UUID字符串 UUID string
    """
    return str(uuid.uuid4())