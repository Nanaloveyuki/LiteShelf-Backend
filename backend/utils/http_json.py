"""
HTTP JSON 工具类
HTTP JSON utilities

"""
# encoding = utf-8
# python 3.13.5

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from loguru import logger
from typing import Dict, Any

class JSONRequestHandler(BaseHTTPRequestHandler):
    """
    JSON 请求处理类
    JSON request handler class
    """
    def _set_headers(self, status_code: int = 200) -> None:
        """
        设置响应头
        Set response headers
        Args:
            status_code (int): 状态码 Status code
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _parse_json(self) -> Dict[str, Any]:
        """
        解析 JSON 请求
        Parse JSON request
        Returns:
            Dict[str, Any]: JSON 数据 JSON data
        """
        try:
            content_length = int(self.headers['Content-Length'])
            json_data = self.rfile.read(content_length)
            return json.loads(json_data)
        except json.JSONDecodeError:
            logger.error(f"解析 JSON 请求失败")
            raise

    def do_GET(self) -> None:
        """
        处理 GET 请求
        Handle GET request
        """
        import re
        from backend.utils.path import get_book_path
        from backend.utils.json import json_load
        
        # 健康检查接口
        if self.path == '/api/health':
            self._set_headers(200)
            self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))
        
        # 获取书籍信息接口
        elif re.match(r'^/api/books/([^/]+)$', self.path):
            book_id = re.match(r'^/api/books/([^/]+)$', self.path).group(1)
            book_path = get_book_path(book_id)
            metadata_path = f"{book_path}/info.json"
            
            try:
                metadata = json_load(metadata_path)
                self._set_headers(200)
                self.wfile.write(json.dumps(metadata).encode('utf-8'))
            except Exception as e:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Book not found', 'details': str(e)}).encode('utf-8'))
        
        # 获取用户信息接口
        elif re.match(r'^/api/users/([^/]+)$', self.path):
            from backend.utils.path import get_user_path
            from backend.utils.json import json_load
            
            user_uid = re.match(r'^/api/users/([^/]+)$', self.path).group(1)
            user_path = get_user_path(user_uid)
            
            try:
                user_info = json_load(user_path)
                # 不返回密码
                user_info.pop('pswd', None)
                self._set_headers(200)
                self.wfile.write(json.dumps(user_info).encode('utf-8'))
            except Exception as e:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'User not found', 'details': str(e)}).encode('utf-8'))
        
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))

    def do_POST(self) -> None:
        """
        处理 POST 请求
        Handle POST request
        """
        # 创建书籍接口
        if self.path == '/api/books':
            try:
                data = self._parse_json()
                from backend.create_book import create_book
                from backend.utils.uuid import generate_uuid
                
                book_id = generate_uuid()
                result = await create_book(
                    book_id=book_id,
                    book_name=data.get('book_name'),
                    user_uid=data.get('user_uid')
                )
                
                self._set_headers(201 if result else 400)
                self.wfile.write(json.dumps({
                    'success': result,
                    'book_id': book_id if result else None
                }).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': 'Internal server error', 'details': str(e)}).encode('utf-8'))
        
        # 创建用户接口
        elif self.path == '/api/users':
            try:
                data = self._parse_json()
                from backend.utils.user import create_user
                
                user_uid = await create_user(
                    user_name=data.get('user_name'),
                    user_pswd=data.get('user_pswd')
                )
                
                self._set_headers(201)
                self.wfile.write(json.dumps({
                    'success': True,
                    'user_uid': user_uid
                }).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': 'Internal server error', 'details': str(e)}).encode('utf-8'))
        
        # 原始数据处理接口
        elif self.path == '/api/data'
            try:
                data = self._parse_json()
                # 处理接收到的JSON数据
                response = {'received': data, 'message': 'Data processed successfully'}
                self._set_headers(status_code=200)
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                self._set_headers(status_code=400)
                self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode('utf-8'))
            except Exception as e:
                self._set_headers(status_code=500)
                logger.error(f"处理 POST 请求失败, 异常信息: {e}")
                self.wfile.write(json.dumps({'error': 'Internal server error', 'details': str(e)}).encode('utf-8'))
        else:
            self._set_headers(status_code=404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
