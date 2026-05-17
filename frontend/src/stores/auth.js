import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  // Thử đọc thông tin user đã lưu trong trình duyệt trước đó (nếu có)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)

  function login(userData) {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  function logout() {
    user.value = null
    localStorage.removeItem('user')
  }

  return { user, login, logout }
})