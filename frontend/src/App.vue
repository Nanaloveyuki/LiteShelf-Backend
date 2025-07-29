<script setup lang="ts">
</script>

<template>
  <!-- 导航栏 - 使用磨砂半透明效果 -->
  <nav class="navbar">
    <div class="logo">LiteShelf</div>
    <div class="nav-links">
      <router-link to="/books">书架</router-link>
      <router-link to="/discover">发现</router-link>
      <router-link to="/settings">设置</router-link>
    </div>
  </nav>

  <!-- 主内容区域 - 路由视图 -->
  <main class="main-content">
    <router-view />
  </main>
</template>

<style scoped>
/* 导航栏样式补充 */
.navbar .logo {
  font-size: 1.2rem;
  font-weight: bold;
}

.navbar .nav-links {
  display: flex;
  gap: 20px;
}

.navbar .nav-links a {
  color: var(--text-main);
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.navbar .nav-links a.router-link-exact-active {
  color: #646cff;
  font-weight: bold;
}

.navbar .nav-links a:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

/* 阅读页面内容样式 */
.reading-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  line-height: 1.8;
  font-size: 1.1rem;
}
</style>
