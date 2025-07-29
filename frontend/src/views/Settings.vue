<template>
  <div class="settings-page">
    <h1>系统设置</h1>
    <div class="settings-section">
      <h2>账户信息</h2>
      <div class="setting-item">
        <label>用户名</label>
        <input type="text" placeholder="输入用户名">
      </div>
      <div class="setting-item">
        <label>邮箱</label>
        <input type="email" placeholder="输入邮箱地址">
      </div>
    </div>
    <div class="settings-section">
      <h2>显示设置</h2>
      <div class="setting-item">
        <label>字体大小</label>
        <select>
          <option>小</option>
          <option>中</option>
          <option>大</option>
        </select>
      </div>
      <div class="setting-item">
        <label>深色模式</label>
        <label class="switch">
          <input type="checkbox">
          <span class="slider round"></span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 设置页面组件
 * Settings page component
 */
</script>

<style scoped>
.settings-page {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.settings-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.settings-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
  color: #666;
}

.setting-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  gap: 10px;
}

.setting-item label {
  flex: 1;
  min-width: 100px;
}

.setting-item input,
.setting-item select {
  flex: 2;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #646cff;
}

input:checked + .slider:before {
  transform: translateX(26px);
}
</style>