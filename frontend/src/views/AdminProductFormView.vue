<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const categories = ref([])

const form = ref({
  ten_san_pham: '', loai: '', don_gia: 0, so_luong: 0, mo_ta: ''
})

// Mảng chứa các file ảnh được người dùng chọn
const imageFiles = ref([])
// Mảng chứa các URL ảnh preview ảo để hiển thị
const previewUrls = ref([])

onMounted(async () => {
  const resCat = await axios.get('http://localhost:8000/store/api/categories/')
  categories.value = resCat.data

  if (route.params.id) {
    const resDetail = await axios.get(`http://localhost:8000/store/api/products/${route.params.id}/`)
    form.value = resDetail.data
    // Load ảnh cũ từ server lên nếu là form sửa
    if (resDetail.data.hinh_anh_url) previewUrls.value.push({ url: resDetail.data.hinh_anh_url, name: 'Ảnh chính' })
  }
})

// Hàm xử lý chọn nhiều ảnh và render Preview
const handleFileChange = (e) => {
  const files = Array.from(e.target.files)
  if (files.length === 0) return

  // Lưu file gốc để gửi API
  imageFiles.value = [...imageFiles.value, ...files]
  
  // Tạo URL ảo để hiển thị Preview ngay lập tức
  files.forEach(file => {
    previewUrls.value.push({ url: URL.createObjectURL(file), name: file.name })
  })
}

// Xóa ảnh khỏi danh sách Preview
const removePreview = (index) => {
  imageFiles.value.splice(index, 1)
  previewUrls.value.splice(index, 1)
}

const saveProduct = async () => {
  const formData = new FormData()
  Object.keys(form.value).forEach(key => formData.append(key, form.value[key]))
  
  // Đẩy toàn bộ mảng ảnh vào FormData
  imageFiles.value.forEach(file => {
    formData.append('hinh_anh', file)
  })

  try {
    if (route.params.id) {
      await axios.post(`http://localhost:8000/store/api/admin/products/edit/${route.params.id}/`, formData)
    } else {
      await axios.post('http://localhost:8000/store/api/admin/products/create/', formData)
    }
    alert('Lưu dữ liệu sản phẩm thành công!')
    router.push('/admin/san-pham')
  } catch (error) {
    alert('Lỗi lưu sản phẩm!')
  }
}
</script>

<template>
  <div style="max-width: 900px; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
    <h2 style="margin-top: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px; color: #1e293b;">
      {{ route.params.id ? 'Sửa thông tin sản phẩm' : 'Thêm sản phẩm mới' }}
    </h2>
    
    <form @submit.prevent="saveProduct" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
      <div style="grid-column: 1/-1;">
        <label style="font-weight: bold; font-size: 14px;">Tên sản phẩm *</label>
        <input type="text" v-model="form.ten_san_pham" required style="width:100%; padding:10px; border-radius:8px; border:1px solid #cbd5e1; margin-top:8px;" />
      </div>
      <div>
        <label style="font-weight: bold; font-size: 14px;">Loại sản phẩm *</label>
        <select v-model="form.loai" required style="width:100%; padding:10px; border-radius:8px; border:1px solid #cbd5e1; margin-top:8px;">
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.ten_loai }}</option>
        </select>
      </div>
      <div>
        <label style="font-weight: bold; font-size: 14px;">Đơn giá (VNĐ) *</label>
        <input type="number" v-model="form.don_gia" required style="width:100%; padding:10px; border-radius:8px; border:1px solid #cbd5e1; margin-top:8px;" />
      </div>
      <div style="grid-column: 1/-1;">
        <label style="font-weight: bold; font-size: 14px;">Mô tả chi tiết</label>
        <textarea v-model="form.mo_ta" style="width:100%; padding:10px; border-radius:8px; border:1px solid #cbd5e1; margin-top:8px; height:80px; resize:none;"></textarea>
      </div>
      
      <div style="grid-column: 1/-1; background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px dashed #cbd5e1;">
        <label style="font-weight: bold; font-size: 14px; display: block; margin-bottom: 15px;">📸 Hình ảnh sản phẩm (Có thể chọn nhiều ảnh)</label>
        
        <input type="file" @change="handleFileChange" accept="image/*" multiple style="margin-bottom: 15px;" />
        
        <div style="display: flex; flex-wrap: wrap; gap: 15px;">
          <div v-for="(preview, idx) in previewUrls" :key="idx" style="position: relative; width: 120px; border: 1px solid #e2e8f0; border-radius: 8px; padding: 5px; background: white; text-align: center;">
            <img :src="preview.url" style="width: 100%; height: 100px; object-fit: contain;" />
            <div style="font-size: 11px; color: #64748b; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 5px;">{{ preview.name }}</div>
            
            <button type="button" @click="removePreview(idx)" style="position: absolute; top: -8px; right: -8px; background: #ef4444; color: white; border: none; width: 22px; height: 22px; border-radius: 50%; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 12px;">×</button>
          </div>
        </div>
      </div>

      <div style="grid-column: 1/-1; margin-top: 15px; border-top: 1px solid #f1f5f9; padding-top: 20px; text-align: right;">
        <button type="button" @click="router.back()" style="background: white; border: 1px solid #cbd5e1; color: #475569; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; margin-right: 12px;">Hủy bỏ</button>
        <button type="submit" style="background: #16a34a; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer;">💾 Lưu thông tin sản phẩm</button>
      </div>
    </form>
  </div>
</template>