<template>
  <div class="bookshelf-container">
  <!-- 创建书籍悬浮按钮 -->
  <button
    class="floating-add-btn"
    @click="showCreateBookModal = true"
    :title="showCreateBookModal ? '关闭创建窗口' : '添加新书籍'"
  >
    <span class="btn-icon">{{ showCreateBookModal ? '✕' : '+' }}</span>
  </button>

  <!-- 创建书籍弹窗 -->
  <div v-if="showCreateBookModal" class="book-modal-overlay">
    <div class="book-modal">
      <div class="modal-header">
        <h2>创建新书籍</h2>
        <button @click="showCreateBookModal = false" class="close-btn">✕</button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleCreateBook">
          <div class="form-group">
            <label for="bookName">书籍名称 *</label>
            <input
              id="bookName"
              v-model="newBook.name"
              type="text"
              required
              placeholder="输入书籍名称"
            >
          </div>
          <div class="form-group">
            <label for="bookAuthor">作者 *</label>
            <input
              id="bookAuthor"
              v-model="newBook.author"
              type="text"
              required
              placeholder="输入作者名称"
            >
          </div>
          <div class="form-group">
            <label for="bookCategory">分类</label>
            <select id="bookCategory" v-model="newBook.category">
              <option value="">选择分类</option>
              <option value="fiction">小说</option>
              <option value="nonfiction">非虚构</option>
              <option value="science">科学</option>
              <option value="history">历史</option>
              <option value="biography">传记</option>
              <option value="other">其他</option>
            </select>
          </div>
          <div class="form-group">
            <label for="bookCover">封面图标</label>
            <input
              id="bookCover"
              type="file"
              accept="image/*"
              @change="handleCoverUpload"
            >
            <div v-if="coverPreview" class="cover-preview">
              <img :src="coverPreview" alt="封面预览">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" @click="showCreateBookModal = false" class="cancel-btn">取消</button>
            <button type="submit" class="create-btn" :disabled="isSubmitting">
              {{ isSubmitting ? '创建中...' : '创建书籍' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
    <!-- 页面标题和搜索区域 -->
    <header class="bookshelf-header">
      <h1 class="page-title">我的书架</h1>
      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索书籍..."
          class="search-input"
          @focus="handleSearchFocus"
          @blur="handleSearchBlur"
        >
      </div>
    </header>

    <!-- 书籍网格展示 -->
    <div v-if="isLoading" class="loading-state">加载中...</div>
    <div v-else-if="errorMsg" class="error-state">{{ errorMsg }}</div>
    <div v-else-if="books.length === 0" class="empty-state">书架为空，添加你的第一本书吧！</div>
    <main v-else class="books-grid" :class="{ 'search-active': isSearchFocused }">
      <div
        v-for="book in filteredBooks"
        :key="book.id"
        class="book-card"
        :class="{ 'completed': book.isCompleted }"
      >
        <!-- 书籍封面 -->
        <div class="book-cover">
          <img
            :src="getBookCover(book.id)"
            :alt="book.name"
            class="cover-image"
            v-if="book.hasCover"
          >
          <div class="placeholder-cover" v-else>
            <span class="cover-placeholder-text">{{ book.name.charAt(0) }}</span>
          </div>
        </div>

        <!-- 书籍信息 -->
        <div class="book-info">
          <h3 class="book-title" :title="book.name">
            {{ book.name }}
          </h3>
          <p class="reading-progress">{{ getReadingProgressText(book) }}</p>
        </div>
      </div>

      <!-- 空状态提示 -->
      <div class="empty-state" v-if="filteredBooks.length === 0">
        <p>没有找到匹配的书籍</p>
        <button class="reset-search" @click="resetSearch">清除搜索</button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, Ref } from 'vue';
import { pinyin } from 'pinyin-pro';
import { bookApi } from '@/api/books';

// 定义书籍类型接口
interface Book {
  id: number;
  name: string;
  author?: string;
  category?: string;
  coverImage?: string;
  readProgress: number;
  chaptersRead: number;
  totalChapters: number;
  isCompleted: boolean;
  hasCover: boolean;
}

// 新书籍表单数据接口
interface NewBookForm {
  name: string;
  author: string;
  category: string;
  coverImage?: File | null;
}

// 状态管理
const searchQuery: Ref<string> = ref('');
const isSearchFocused: Ref<boolean> = ref(false);
const books: Ref<Book[]> = ref<Book[]>([]);
const isLoading = ref(false);
const errorMsg = ref('');
// 创建书籍相关状态
const showCreateBookModal = ref(false);
const isSubmitting = ref(false);
const coverPreview = ref('');
const newBook = ref<NewBookForm>({
  name: '',
  author: '',
  category: '',
  coverImage: null
});

// 初始化书籍数据
onMounted(async () => {
  try {
    isLoading.value = true;
    const data = await bookApi.getAllBooks();
    books.value = data;
  } catch (err) {
    errorMsg.value = '获取书籍数据失败，请刷新页面重试';
    console.error('Failed to fetch books:', err);
  } finally {
    isLoading.value = false;
  }
});

// 搜索功能 - 支持拼音搜索
const filteredBooks = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return books.value;

  return books.value.filter(book => {
    // 检查书名是否包含搜索词
    const nameMatch = book.name.toLowerCase().includes(query);
    if (nameMatch) return true;

    // 检查拼音是否包含搜索词
    const pinyinName = pinyin(book.name, { type: 'string', tone: false }).toLowerCase();
    return pinyinName.includes(query);
  });
});

// 搜索框焦点处理
const handleSearchFocus = () => {
  isSearchFocused.value = true;
};

const handleSearchBlur = () => {
  // 如果搜索框为空则失去焦点时关闭搜索状态
  if (!searchQuery.value.trim()) {
    isSearchFocused.value = false;
  }
};

// 重置搜索
const resetSearch = () => {
  searchQuery.value = '';
  isSearchFocused.value = false;
};

// 处理封面上传预览
const handleCoverUpload = (e: Event) => {
  const input = e.target as HTMLInputElement;
  if (input.files && input.files[0]) {
    const file = input.files[0];
    newBook.value.coverImage = file;
    const reader = new FileReader();
    reader.onload = (event) => {
      coverPreview.value = event.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

// 处理创建书籍表单提交
const handleCreateBook = async () => {
  try {
    isSubmitting.value = true;
    // 创建FormData对象来处理文件上传
    const formData = new FormData();
    formData.append('name', newBook.value.name);
    formData.append('author', newBook.value.author);
    formData.append('category', newBook.value.category || 'other');
    
    if (newBook.value.coverImage) {
      formData.append('cover', newBook.value.coverImage);
    }

    // 调用API创建新书籍
    const createdBook = await bookApi.addBook(formData);
    
    // 添加到书籍列表
    books.value.push({
      ...createdBook,
      readProgress: 0,
      chaptersRead: 0,
      totalChapters: 0,
      isCompleted: false,
      hasCover: !!createdBook.coverImage
    });

    // 重置表单并关闭弹窗
    newBook.value = {
      name: '',
      author: '',
      category: '',
      coverImage: null
    };
    coverPreview.value = '';
    showCreateBookModal.value = false;
  } catch (err) {
    console.error('创建书籍失败:', err);
    errorMsg.value = '创建书籍失败，请重试';
  } finally {
    isSubmitting.value = false;
  }
}

// 获取书籍封面图片
const getBookCover = (bookId: number): string => {
  // 使用picsum.photos提供随机封面图片
  return `https://picsum.photos/seed/book${bookId}/300/450`;
};

// 获取阅读进度文本
const getReadingProgressText = (book: Book): string => {
  if (book.readProgress === 0) return '未开始阅读';
  if (book.isCompleted) return '已读完';
  return `已读 ${book.readProgress}%`;
};
</script>

<style scoped lang="scss">
.bookshelf-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.bookshelf-header {
  padding: 20px 0;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: clamp(1.2rem, 5vw, 2rem);
  color: #333;
  margin: 0;
}

.search-box {
  width: 300px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1.125rem;
  border: 1px solid #ddd;
  border-radius: 24px;
  font-size: clamp(0.8rem, 2.5vw, 1rem);
  transition: all 0.3s ease;
  outline: none;

  &:focus {
    border-color: #42b983;
    box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.2);
  }
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 25px;
  transition: all 0.3s ease;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;

  &.search-active {
    margin-top: 20px;
  }
}

.book-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }

  &.completed {
    border: 2px solid #42b983;
  }
}

.book-cover {
  height: 220px;
  background-color: #f5f5f5;
  position: relative;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-cover {
  width: 100%;
  height: 100%;
  background-color: #42b983;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-placeholder-text {
  color: white;
  font-size: 48px;
  font-weight: bold;
}

.book-info {
  padding: 15px;
}

.book-title {
  font-size: clamp(0.9rem, 3vw, 1.2rem);
  color: #333;
  margin: 0 0 0.5rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.reading-progress {
  font-size: clamp(0.8rem, 2.5vw, 1rem);
  color: #666;
  margin: 0;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.reset-search {
  margin-top: 15px;
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #359469;
  }
}

/* 响应式调整 - 使用rem单位实现自适应缩放 */
/* 基础样式使用16px基准值 */
html { font-size: 16px; }

/* 高像素密度设备 */
@media (min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  html { font-size: 20px; }
}

/* 超高像素密度移动设备 */
@media (min-device-pixel-ratio: 3) and (max-width: 480px) {
  html { font-size: 24px; }
}

/* 低像素密度小屏设备 */
@media (max-device-pixel-ratio: 1.5) and (max-width: 320px) {
  html { font-size: 22px; }
}

/* 平板设备 */
@media (max-width: 768px) {
  html { font-size: 17px; }
  .bookshelf-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-box { width: 100%; margin-top: 15px; }

  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 20px;
  }
}

/* 手机设备 */
@media (max-width: 480px) {
  html { font-size: 19px; }
  .bookshelf-container { padding: 10px; }
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 12px;
  }
  .book-cover { height: 180px; }
  .book-info {
  padding: 0.75rem;
}
  .empty-state { padding: 40px 10px; }
}

/* 超小屏幕手机设备 */
@media (max-width: 320px) {
  html { font-size: 20px; }
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }
  .book-cover { height: 160px; }
  .search-input { padding: 14px 20px; }
}
</style>