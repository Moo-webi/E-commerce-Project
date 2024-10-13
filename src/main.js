import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// Set the base URL for Axios globally
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// Create a global property for axios
const app = createApp(App)
app.config.globalProperties.$axios = axios

// Use router and store
app.use(store)
app.use(router)

// Mount the app
app.mount('#app')

