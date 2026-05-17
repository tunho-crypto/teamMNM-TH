<script setup>
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
</script>

<template>
  <div style="text-align: left;">
    <h2 style="color: #1e293b; margin-top: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px;">
      📊 TỔNG QUAN HỆ THỐNG
    </h2>
    
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 20px;">
      <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
        <h3 style="margin: 0; font-size: 14px; color: #64748b; text-transform: uppercase;">Tổng đơn hàng</h3>
        <p style="font-size: 28px; font-weight: 800; margin: 10px 0 0 0; color: #0f172a;">1,254</p>
      </div>
      <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border-left: 5px solid #10b981; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
        <h3 style="margin: 0; font-size: 14px; color: #64748b; text-transform: uppercase;">Doanh thu tháng</h3>
        <p style="font-size: 28px; font-weight: 800; margin: 10px 0 0 0; color: #10b981;">450M</p>
      </div>
      <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border-left: 5px solid #f59e0b; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
        <h3 style="margin: 0; font-size: 14px; color: #64748b; text-transform: uppercase;">Khách hàng mới</h3>
        <p style="font-size: 28px; font-weight: 800; margin: 10px 0 0 0; color: #0f172a;">128</p>
      </div>
      <div style="background: #fff1f2; padding: 20px; border-radius: 12px; border-left: 5px solid #ef4444; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
        <h3 style="margin: 0; font-size: 14px; color: #9f1239; text-transform: uppercase;">Sản phẩm hết hàng</h3>
        <p style="font-size: 28px; font-weight: 800; margin: 10px 0 0 0; color: #ef4444;">12</p>
      </div>
    </div>

    <div style="margin-top: 40px; background: #fff; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center;">
      <div style="font-size: 60px;">🏢</div>
      <h3 style="color: #1e293b;">Chào mừng {{ authStore.user?.ho_ten }} đến với Trung tâm điều hành</h3>
      <p style="color: #64748b;">Sếp có thể chọn các chức năng Quản lý Sản phẩm, Đơn hàng, Tồn kho ở menu bên trái nhé.</p>
    </div>
  </div>
</template>