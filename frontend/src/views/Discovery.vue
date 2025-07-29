<template>
  <div class="discovery-page">
    <h1>发现好书</h1>
    <div class="category-filter">
      <button class="active">推荐</button>
      <button>小说</button>
      <button>科技</button>
      <button>历史</button>
    </div>
    <div class="book-list">
      <!-- 发现页面内容将在这里动态生成 -->
      <div class="book-item">推荐书籍 1</div>
      <div class="book-item">推荐书籍 2</div>
      <div class="book-item">推荐书籍 3</div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 发现页面组件
 * Discovery page component
 */
</script>

<style scoped>
.discovery-page {
  padding: 20px;
}

.category-filter {
  display: flex;
  gap: 10px;
  margin: 20px 0;
  flex-wrap: wrap;
}

.category-filter button {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
}

.category-filter button.active {
  background-color: #646cff;
  color: white;
}

.book-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.book-item {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>