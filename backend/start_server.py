"""
LiteShelf服务器启动程序
LiteShelf server startup program

"""
# encoding = utf-8
# python 3.13.5

import sys
import os
from http.server import HTTPServer
from loguru import logger

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.utils import JSONRequestHandler

def run_server(host: str = 'localhost', port: int = 8000) -> None:
    """
    启动HTTP服务器
    Start HTTP server
    Args:
        host (str): 主机地址 Host address
        port (int): 端口号 Port number
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, JSONRequestHandler)
    logger.info(f"服务器启动成功, 地址: {host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("服务器关闭中...")
        httpd.server_close()
        logger.info("服务器已关闭")
    except Exception as e:
        logger.error(f"服务器运行异常, 异常信息: {e}")
        httpd.server_close()
        logger.error("服务器关闭")

if __name__ == '__main__':
    run_server()