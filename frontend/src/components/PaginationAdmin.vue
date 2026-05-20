<script setup>
const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true }
})
const emit = defineEmits(['changePage'])

const goToPage = (page) => {
  if (page >= 1 && page <= props.totalPages) {
    emit('changePage', page)
  }
}
</script>

<template>
  <div class="pagination" v-if="totalPages > 1">
    <a href="#" @click.prevent="goToPage(1)" v-if="currentPage > 1">&laquo; Đầu</a>
    <a href="#" @click.prevent="goToPage(currentPage - 1)" v-if="currentPage > 1">‹ Trước</a>

    <span class="active">Trang {{ currentPage }} / {{ totalPages }}</span>

    <a href="#" @click.prevent="goToPage(currentPage + 1)" v-if="currentPage < totalPages">Sau ›</a>
    <a href="#" @click.prevent="goToPage(totalPages)" v-if="currentPage < totalPages">Cuối &raquo;</a>
  </div>
</template>

<style scoped>
.pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 25px; }
.pagination a, .pagination span { padding: 8px 14px; border: 1px solid #cbd5e1; border-radius: 8px; text-decoration: none; color: #475569; font-weight: 600; font-size: 14px; transition: 0.2s; }
.pagination a:hover { background: #f1f5f9; border-color: #94a3b8; }
.pagination .active { background: #008a37; color: white; border-color: #008a37; }
</style>