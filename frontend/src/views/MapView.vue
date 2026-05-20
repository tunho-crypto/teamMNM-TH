<script setup>
import { ref, onMounted, shallowRef } from 'vue'
import axios from 'axios'

const stores = ref([])
const searchKeyword = ref('')
const searchAddress = ref('')
const radiusSelect = ref('5')
const addressSuggestions = ref([])

// Khai báo các biến lưu trữ lõi bản đồ (Dùng shallowRef để Vue không làm lag Leaflet)
const map = shallowRef(null)
const markers = shallowRef(null)
const userMarker = shallowRef(null)
const routingControl = shallowRef(null)
const radiusCircle = shallowRef(null)
const userLatLng = shallowRef(null)

const sidebarVisible = ref(false)
const sidebarRadiusStores = ref([])
const statusBarMessage = ref('')

// Hàm nhúng thư viện tự động
const loadMapLibraries = () => {
  return new Promise((resolve) => {
    if (window.L && window.L.Routing) return resolve()
    
    // CSS
    const links = [
      'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
      'https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.css',
      'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css',
      'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css'
    ]
    links.forEach(href => {
      const link = document.createElement('link')
      link.rel = 'stylesheet'; link.href = href
      document.head.appendChild(link)
    })

    // JS
    const script1 = document.createElement('script')
    script1.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script1.onload = () => {
      const script2 = document.createElement('script')
      script2.src = 'https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.js'
      script2.onload = () => {
        const script3 = document.createElement('script')
        script3.src = 'https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js'
        script3.onload = resolve
        document.body.appendChild(script3)
      }
      document.body.appendChild(script2)
    }
    document.body.appendChild(script1)
  })
}

onMounted(async () => {
  await loadMapLibraries()
  const L = window.L

  // Khởi tạo bản đồ
  map.value = L.map('map').setView([10.7769, 106.7009], 13)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { maxZoom: 19 }).addTo(map.value)

  // Load danh sách cửa hàng
  const res = await axios.get('http://localhost:8000/store/api/branches/')
  stores.value = res.data

  const storeIcon = L.divIcon({
    html: `<div style="background-color: #008a37; width: 32px; height: 32px; border-radius: 50% 50% 50% 0; transform: rotate(-45deg); border: 2px solid white; box-shadow: -2px 2px 5px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center;"><span style="transform: rotate(45deg); font-size: 16px;">🛒</span></div>`,
    className: '', iconSize: [36, 36], iconAnchor: [18, 36], popupAnchor: [0, -36]
  })

  markers.value = L.markerClusterGroup({ chunkedLoading: true, maxClusterRadius: 50 })

  stores.value.forEach(st => {
    if(st.latitude && st.longitude) {
      st.markerObj = L.marker([st.latitude, st.longitude], {icon: storeIcon})
      capNhatPopup(st, null)
      markers.value.addLayer(st.markerObj)
    }
  })
  map.value.addLayer(markers.value)
})

const capNhatPopup = (store, distanceKm) => {
  const distHtml = distanceKm ? `<br><b>📍 Cách bạn: ${distanceKm} km</b>` : ``
  const content = `<div style="text-align:center"><b style="color:#008a37; font-size: 1.1em">${store.ten_chi_nhanh}</b><br><small>${store.dia_chi}</small>${distHtml}
    <div style="display:flex; gap:5px; margin-top:10px;">
      <button onclick="window.dispatchEvent(new CustomEvent('chi-duong', {detail: {lat: ${store.latitude}, lon: ${store.longitude}, ten: '${store.ten_chi_nhanh}'}}))" style="flex:1; background:#008a37; color:white; border:none; padding:8px; border-radius:4px; font-weight:bold; cursor:pointer;">🚗 Chỉ đường</button>
    </div></div>`
  store.markerObj.bindPopup(content)
}

// Bắt sự kiện từ HTML Popup trong Leaflet
window.addEventListener('chi-duong', (e) => veDuong(e.detail.lat, e.detail.lon, e.detail.ten))

// Gợi ý địa chỉ Nominatim API
let timeoutId = null
const goiYDiaChi = () => {
  clearTimeout(timeoutId)
  if (searchAddress.value.length < 3) { addressSuggestions.value = []; return }
  timeoutId = setTimeout(async () => {
    const res = await axios.get(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchAddress.value)}&countrycodes=vn&limit=5`)
    addressSuggestions.value = res.data
  }, 600)
}

const chonDiaChiGoiy = (item) => {
  searchAddress.value = item.display_name
  addressSuggestions.value = []
  capNhatViTriUser(parseFloat(item.lat), parseFloat(item.lon))
  map.value.setView([parseFloat(item.lat), parseFloat(item.lon)], 15)
}

const capNhatViTriUser = (lat, lon) => {
  const L = window.L
  userLatLng.value = L.latLng(lat, lon)
  if (userMarker.value) map.value.removeLayer(userMarker.value)
  userMarker.value = L.marker(userLatLng.value, {draggable: true}).addTo(map.value)
  userMarker.value.bindPopup("<b>Vị trí của bạn</b>").openPopup()
  stores.value.forEach(st => capNhatPopup(st, (userLatLng.value.distanceTo(L.latLng(st.latitude, st.longitude)) / 1000).toFixed(2)))
  userMarker.value.on('dragend', () => capNhatViTriUser(userMarker.value.getLatLng().lat, userMarker.value.getLatLng().lng))
}

const layViTriGPS = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => { capNhatViTriUser(pos.coords.latitude, pos.coords.longitude); map.value.setView([pos.coords.latitude, pos.coords.longitude], 14) },
      err => alert("Lỗi GPS.")
    )
  }
}

const veDuong = (lat, lon, tenStore) => {
  if (!userLatLng.value) return alert("Vui lòng đặt vị trí của bạn trước!")
  const L = window.L
  if (routingControl.value) map.value.removeControl(routingControl.value)
  
  routingControl.value = L.Routing.control({
    waypoints: [userLatLng.value, L.latLng(lat, lon)], 
    createMarker: () => null,
    router: L.Routing.osrmv1({ serviceUrl: 'https://routing.openstreetmap.de/routed-bike/route/v1', language: 'vi', routingOptions: { alternatives: true } }),
    lineOptions: { styles: [{color: '#008a37', opacity: 0.8, weight: 6}] },
    fitSelectedRoutes: true, routeWhileDragging: false 
  }).addTo(map.value)
}

const timCuaHangTrongBanKinh = () => {
  if (!userLatLng.value) return alert("Bấm nút Dùng GPS để định vị sếp trước!")
  const L = window.L
  const radiusMeters = parseFloat(radiusSelect.value) * 1000

  if (radiusCircle.value) map.value.removeLayer(radiusCircle.value)
  radiusCircle.value = L.circle(userLatLng.value, { color: '#d8232a', fillColor: '#ffe100', fillOpacity: 0.15, radius: radiusMeters }).addTo(map.value)

  const foundStores = stores.value.map(st => {
    return { store: st, dist: userLatLng.value.distanceTo(L.latLng(st.latitude, st.longitude)) }
  }).filter(item => item.dist <= radiusMeters).sort((a, b) => a.dist - b.dist)

  sidebarRadiusStores.value = foundStores
  sidebarVisible.value = true
  map.value.fitBounds(radiusCircle.value.getBounds(), { padding: [50, 50] })
}
</script>

<template>
  <div id="map-wrapper" style="text-align: left;">
    <div class="control-bar">
      <div class="search-container" style="position: relative;">
          <input type="text" v-model="searchAddress" @input="goiYDiaChi" class="search-input" placeholder="Nhập địa chỉ của bạn...">
          <ul v-if="addressSuggestions.length" class="suggestions-list" style="display: block;">
            <li v-for="item in addressSuggestions" :key="item.place_id" @click="chonDiaChiGoiy(item)">{{ item.display_name }}</li>
          </ul>
      </div>

      <div class="search-container" style="min-width: 180px; flex-grow: 0;">
          <select v-model="radiusSelect" class="search-input">
              <option value="1">Bán kính 1 km</option>
              <option value="3">Bán kính 3 km</option>
              <option value="5">Bán kính 5 km</option>
              <option value="10">Bán kính 10 km</option>
          </select>
          <button class="search-btn" style="background-color: #d8232a;" @click="timCuaHangTrongBanKinh">🎯 Tìm quanh đây</button>
      </div>

      <button class="btn-nearest" style="background-color: #ffe100; color: #d8232a; font-weight: bold; padding: 10px; border: none; border-radius: 4px; cursor: pointer;" @click="layViTriGPS">📡 Dùng GPS</button>
    </div>

    <div class="map-body" style="display: flex; height: calc(100vh - 150px);">
      <div v-show="sidebarVisible" id="sidebar" style="width: 320px; background: white; border-right: 1px solid #ddd; overflow-y: auto;">
          <div class="sidebar-header" style="background: #008a37; color: white; padding: 15px; display: flex; justify-content: space-between;">
              <span>Có {{ sidebarRadiusStores.length }} cửa hàng</span>
              <span style="cursor: pointer;" @click="sidebarVisible = false; map.removeLayer(radiusCircle)">✕</span>
          </div>
          <div style="padding: 10px;">
            <div v-for="item in sidebarRadiusStores" :key="item.store.id" style="padding: 15px; border-bottom: 1px solid #eee;">
              <div style="color: #008a37; font-weight: bold;">{{ item.store.ten_chi_nhanh }}</div>
              <div style="font-size: 13px; margin-bottom: 5px;">{{ item.store.dia_chi }}</div>
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #d8232a; font-weight: bold;">📍 {{ (item.dist / 1000).toFixed(2) }} km</span>
                <button @click="veDuong(item.store.latitude, item.store.longitude, item.store.ten_chi_nhanh)" style="background: #f39c12; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">🚗 Chỉ đường</button>
              </div>
            </div>
          </div>
      </div>
      
      <div id="map" style="flex-grow: 1; width: 100%; z-index: 1;"></div>
    </div>
  </div>
</template>

<style scoped>
.control-bar { background-color: #f8f9fa; padding: 15px 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 15px; border-bottom: 1px solid #ddd; z-index: 1000; position: relative;}
.search-container { display: flex; flex-grow: 1; min-width: 200px; }
.search-input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px 0 0 4px; outline: none; }
.search-btn { padding: 10px 15px; color: white; border: none; border-radius: 0 4px 4px 0; cursor: pointer; font-weight: bold; white-space: nowrap; }
.suggestions-list { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #ccc; max-height: 250px; overflow-y: auto; list-style: none; padding: 0; margin: 0; z-index: 2000; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 0 0 4px 4px; }
.suggestions-list li { padding: 10px; cursor: pointer; border-bottom: 1px solid #eee; font-size: 14px; }
.suggestions-list li:hover { background-color: #e6f7ff; color: #0050b3; }
</style>