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
        
        # 获取所有书籍接口
        elif self.path == '/api/books':
            from backend.utils.path import get_books_dir
            from backend.utils.file import list_dir
            import os
            
            books_dir = get_books_dir()
            books = []
            
            if os.path.exists(books_dir):
                for book_id in list_dir(books_dir):
                    book_path = os.path.join(books_dir, book_id)
                    metadata_path = os.path.join(book_path, 'info.json')
                    try:
                        metadata = json_load(metadata_path)
                        books.append(metadata)
                    except Exception as e:
                        logger.warning(f'Failed to load book {book_id}: {str(e)}')
            
            self._set_headers(200)
            self.wfile.write(json.dumps(books).encode('utf-8'))
        
        # 获取单本书籍信息接口
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
                content_type = self.headers.get('Content-Type', '')
                if 'multipart/form-data' in content_type:
                    # 解析表单数据
                    import cgi
                    import os
                    from backend.utils.path import get_book_path
                    from backend.utils.uuid import generate_uuid
                    from backend.utils.file import create_directory
                    from backend.utils.json import json_dump

                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
                    )

                    fields = {key: form.getvalue(key) for key in form.keys() if key in ['name', 'author', 'category', 'user_uid']}
                    files = {key: form[key] for key in form.keys() if key == 'cover' and form[key].filename}

                    # 验证必填字段
                    if not fields.get('name') or not fields.get('author') or not fields.get('user_uid'):
                        self._set_headers(400)
                        self.wfile.write(json.dumps({'error': '书籍名称、作者和用户ID为必填项'}).encode('utf-8'))
                        return

                    # 生成书籍ID
                    book_id = generate_uuid()
                    book_path = get_book_path(book_id)
                    create_directory(book_path)

                    # 保存封面图片
                    cover_path = None
                    if 'cover' in files:
                        cover_file = files['cover']
                        ext = os.path.splitext(cover_file.filename)[1].lower()
                        if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                            self._set_headers(400)
                            self.wfile.write(json.dumps({'error': '不支持的图片格式'}).encode('utf-8'))
                            return
                        cover_path = os.path.join(book_path, f'cover{ext}')
                        with open(cover_path, 'wb') as f:
                            f.write(cover_file.file.read())

                    # 准备书籍数据
                    book_data = {
                        'id': book_id,
                        'name': fields['name'],
                        'author': fields['author'],
                        'category': fields.get('category', 'other'),
                        'user_uid': fields['user_uid'],
                        'coverImage': cover_path.replace(os.path.abspath(''), '')[1:] if cover_path else None,
                        'readProgress': 0,
                        'chaptersRead': 0,
                        'totalChapters': 0,
                        'isCompleted': False,
                        'hasCover': bool(cover_path)
                    }

                    # 保存书籍信息
                    json_dump(os.path.join(book_path, 'info.json'), book_data)
                    self._set_headers(201)
                    self.wfile.write(json.dumps({
                        'success': True,
                        'book_id': book_id
                    }).encode('utf-8'))

                # 处理JSON数据（保持原有支持）
                else:
                    # 处理JSON数据
                    import os
                    from backend.utils.path import get_book_path
                    from backend.utils.uuid import generate_uuid
                    from backend.utils.file import create_directory
                    from backend.utils.json import json_dump

                    data = self._parse_json()

                    # 验证必填字段
                    if not data.get('name') or not data.get('author') or not data.get('user_uid'):
                        self._set_headers(400)
                        self.wfile.write(json.dumps({'error': '书籍名称、作者和用户ID为必填项'}).encode('utf-8'))
                        return

                    # 生成书籍ID
                    book_id = generate_uuid()
                    book_path = get_book_path(book_id)
                    # 使用同步文件操作
                    import os
                    import json
                    os.makedirs(book_path, exist_ok=True)

                    # 准备书籍数据
                    book_data = {
                        'id': book_id,
                        'name': data.get('name', 'Unnamed Book'),
                        'author': data.get('author', ''),
                        'category': data.get('category', 'other'),
                        'user_uid': data.get('user_uid'),
                        'coverImage': None,
                        'readProgress': 0,
                        'chaptersRead': 0,
                        'totalChapters': 0,
                        'isCompleted': False,
                        'hasCover': False
                    }

                    # 保存书籍信息
                    with open(os.path.join(book_path, 'info.json'), 'w', encoding='utf-8') as f:
                        json.dump(book_data, f, ensure_ascii=False, indent=2)
                    self._set_headers(201)
                    self.wfile.write(json.dumps({
                        'success': True,
                        'book_id': book_id
                    }).encode('utf-8'))

            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': 'Internal server error', 'details': str(e)}).encode('utf-8'))
        
        # 创建用户接口
        elif self.path == '/api/users':
            try:
                data = self._parse_json()
                from backend.utils.user import create_user
                
                user_uid = create_user(
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
        elif self.path == '/api/data':
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
                logger.error(f"处理 POST 请求失败,异常信息: {e}")
                self.wfile.write(json.dumps({'error': 'Internal server error', 'details': str(e)}).encode('utf-8'))
        else:
            self._set_headers(status_code=404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
    
    def do_PUT(self) -> None:
        """
        处理 PUT 请求
        Handle PUT request
        """
        import re
        from backend.utils.user import update_user_profile
        
        # 更新用户资料接口
        if re.match(r'^/api/users/([^/]+)/profile$', self.path):
            user_uid = re.match(r'^/api/users/([^/]+)/profile$', self.path).group(1)
            try:
                data = self._parse_json()
                # 提取需要更新的字段 Extract fields to update
                update_fields = {}
                if 'avatar_url' in data:
                    update_fields['avatar_url'] = data['avatar_url']
                if 'bio' in data:
                    update_fields['bio'] = data['bio']
                
                success = update_user_profile(user_uid, **update_fields)
                self._set_headers(200 if success else 400)
                self.wfile.write(json.dumps({
                    'success': success,
                    'message': 'Profile updated successfully' if success else 'Failed to update profile'
                }).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': 'Internal server error', 'details': str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
