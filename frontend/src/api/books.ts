import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 书籍相关API接口
export const bookApi = {
  /**
   * 获取所有书籍
   * Get all books
   */
  getAllBooks: async () => {
    const response = await api.get('/books');
    return response.data;
  },

  /**
   * 获取单本书籍详情
   * Get book details
   * @param id - 书籍ID
   */
  getBookById: async (id: number) => {
    const response = await api.get(`/books/${id}`);
    return response.data;
  },

  /**
   * 添加新书籍
   * Add new book
   * @param book - 书籍信息
   */
  addBook: async (book: any) => {
    const response = await api.post('/books', book);
    return response.data;
  },

  /**
   * 更新书籍阅读进度
   * Update book reading progress
   * @param id - 书籍ID
   * @param progress - 阅读进度
   */
  updateReadingProgress: async (id: number, progress: number) => {
    const response = await api.patch(`/books/${id}/progress`, { progress });
    return response.data;
  },

  /**
   * 删除书籍
   * Delete book
   * @param id - 书籍ID
   */
  deleteBook: async (id: number) => {
    const response = await api.delete(`/books/${id}`);
    return response.data;
  }
};

export default api;