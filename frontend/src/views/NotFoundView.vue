<template>
  <div style="font-family: 'Segoe UI', Arial, sans-serif; min-height: 80vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at top left, rgba(34, 197, 94, 0.18), transparent 30%), linear-gradient(135deg, #f8fafc, #eef6ff); padding: 24px;">
    <div style="width: 100%; max-width: 680px; background: rgba(255, 255, 255, 0.92); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 28px; padding: 48px; text-align: center; box-shadow: 0 20px 40px rgba(15, 23, 42, 0.04);">
      <div style="display: inline-block; padding: 6px 16px; background: #fee2e2; color: #ef4444; font-size: 13px; font-weight: 700; border-radius: 20px; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 20px;">Trang không tồn tại</div>
      <div style="font-size: 64px; margin-bottom: 10px;">🛒</div>
      <div style="font-size: 110px; font-weight: 900; line-height: 1; color: transparent; -webkit-text-stroke: 2px #cbd5e1; margin-bottom: 16px;">404</div>
      <h1 style="font-size: 32px; color: #0f172a; margin-bottom: 16px;">Ôi, không tìm thấy trang này</h1>
      <p style="font-size: 17px; color: #475569; line-height: 1.6; max-width: 480px; margin: 0 auto 32px auto;">Có thể đường dẫn bạn vừa truy cập không còn tồn tại, đã bị thay đổi hoặc nhập chưa chính xác.</p>
      
      <router-link to="/" style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 14px 28px; font-size: 16px; font-weight: 600; color: #2563eb; background: #fff; border: 1px solid #dbeafe; border-radius: 12px; text-decoration: none;">
        Về Trang Chủ
      </router-link>
    </div>
  </div>
</template>