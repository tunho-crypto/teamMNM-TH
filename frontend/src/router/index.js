import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // --- CÁC TRANG DÀNH CHO KHÁCH HÀNG ---
  { path: '/', name: 'Home', component: () => import('../views/HomeView.vue') },
  { path: '/san-pham', name: 'ProductList', component: () => import('../views/ProductListView.vue') },
  { path: '/san-pham/:id', name: 'ProductDetail', component: () => import('../views/ProductDetailView.vue') },
  { path: '/ban-do', name: 'MapSearch', component: () => import('../views/MapView.vue') },
  { path: '/cua-hang', name: 'StoreList', component: () => import('../views/StoreListView.vue') },
  { path: '/cua-hang/:id', name: 'StoreDetail', component: () => import('../views/StoreDetailView.vue') },
  { path: '/gioi-thieu', name: 'About', component: () => import('../views/AboutView.vue') },
  { path: '/dang-nhap', name: 'Login', component: () => import('../views/LoginView.vue') },
  { path: '/dang-ky', name: 'Register', component: () => import('../views/RegisterView.vue') },
  { path: '/xac-thuc-otp', name: 'VerifyOTP', component: () => import('../views/VerifyOTPView.vue') },
  { path: '/gio-hang', name: 'CartDetail', component: () => import('../views/CartView.vue') },
  { path: '/lich-su', name: 'OrderHistory', component: () => import('../views/OrderHistoryView.vue') },
 {
  path: '/quen-mat-khau',
  component: () => import('../views/ForgotPasswordView.vue')
},
  // --- CÁC TRANG BÁN HÀNG TẠI QUẦY (POS) ---
  { path: '/pos', name: 'PosCheckout', component: () => import('../views/PosCheckoutView.vue') },
  { path: '/pos/hoa-don', name: 'PosInvoice', component: () => import('../views/PosInvoiceView.vue') },

  // --- TRANG LỖI ---
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('../views/NotFoundView.vue') },

  // --- PHÂN HỆ QUẢN TRỊ ADMIN (Đã sửa lỗi và bổ sung đầy đủ trang) ---
  {
    path: '/admin',
    component: () => import('../views/AdminLayout.vue'),
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard', component: () => import('../views/DashboardView.vue') },
      { path: 'san-pham', component: () => import('../views/AdminProductListView.vue') },
      { path: 'san-pham/them', component: () => import('../views/AdminProductFormView.vue') },
      { path: 'san-pham/sua/:id', component: () => import('../views/AdminProductFormView.vue') },
      { path: 'don-hang', component: () => import('../views/AdminOrderListView.vue') },
      { path: 'ton-kho', component: () => import('../views/AdminInventoryView.vue') },
      { path: 'tai-khoan', component: () => import('../views/AdminAccountListView.vue') },
      
      // Bổ sung 3 dòng này để hết lỗi không vào được trang sếp nhé:
      { path: 'khach-hang', component: () => import('../views/AdminCustomerListView.vue') },
      { path: 'nhan-vien', component: () => import('../views/AdminEmployeeListView.vue') },
      { path: 'chi-nhanh', component: () => import('../views/AdminBranchListView.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router