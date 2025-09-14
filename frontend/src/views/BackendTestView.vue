<template>
  <div class="backend-test">
    <h1>🔧 Backend Integration Test</h1>
    
    <!-- Scene Information -->
    <div class="scene-info">
      <h3>📊 Scene Information</h3>
      <div class="badges">
        <span class="badge" :class="sceneBadgeClass">Backend: {{ context }}</span>
      </div>
    </div>
    
    <!-- API Testing -->
    <div class="api-test">
      <h3>🎯 API Testing</h3>
      <div class="controls">
        <input 
          v-model="userName" 
          type="text" 
          placeholder="Enter your name"
          class="name-input"
        />
        <button @click="testSayHello" :disabled="loading" class="btn primary">
          👋 Say Hello
        </button>
        <button @click="testSayHelloAsync" :disabled="loading" class="btn primary">
          ⏳ Say Hello Async
        </button>
        <button @click="clearResults" class="btn secondary">
          🗑️ Clear
        </button>
      </div>
      
      <!-- Backend Switching -->
      <div class="backend-switching">
        <strong>🔄 Test different backends:</strong>
        <a href="#backend_type=mock">Mock</a> |
        <a href="#backend_type=webview">WebView</a> |
        <a href="#backend_type=webui">WebUI</a> |
        <a href="#backend_type=qt">Qt4</a>
      </div>
    </div>
    
    <!-- Results -->
    <div class="results">
      <h3>📋 Results</h3>
      <div class="results-container" ref="resultsContainer">
        <div v-for="(result, index) in results" :key="index" :class="['result-item', result.type]">
          <span class="timestamp">[{{ result.timestamp }}]</span>
          <span class="message">{{ result.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { 
  createBackend, 
  type BackendInterface 
} from '../api/backend-abstraction'

// Reactive state
const userName = ref('World')
const loading = ref(false)
const results = ref<Array<{ timestamp: string, message: string, type: string }>>([])
const resultsContainer = ref<HTMLElement>()

// Backend instance
let backend: BackendInterface

// Context information
const context = ref(getContext())

// Computed properties
const sceneBadgeClass = computed(() => ({ on: true }))

// Logging function
const log = (message: string, type: 'info' | 'success' | 'error' = 'info') => {
  const timestamp = new Date().toLocaleTimeString()
  results.value.push({ timestamp, message, type })
  
  // Auto scroll to bottom
  nextTick(() => {
    if (resultsContainer.value) {
      resultsContainer.value.scrollTop = resultsContainer.value.scrollHeight
    }
  })
}

// Initialize backend
const initBackend = () => {
  try {
    backend = createBackend()
    log(`Backend initialized: ${context.value}`, 'success')
  } catch (error) {
    log(`Failed to initialize backend: ${error}`, 'error')
  }
}

// API test methods
const testSayHello = async () => {
  if (!userName.value.trim()) {
    log('Please enter a name', 'error')
    return
  }
  
  loading.value = true
  try {
    log(`Testing say_hello("${userName.value}")...`, 'info')
    const response = await backend.say_hello(userName.value)
    log(`Response: ${response}`, 'success')
  } catch (error) {
    log(`Error: ${error}`, 'error')
  } finally {
    loading.value = false
  }
}

const testSayHelloAsync = async () => {
  if (!userName.value.trim()) {
    log('Please enter a name', 'error')
    return
  }
  
  loading.value = true
  try {
    log(`Testing say_hello_async("${userName.value}")...`, 'info')
    const response = await backend.say_hello_async(userName.value)
    log(`Response: ${response}`, 'success')
  } catch (error) {
    log(`Error: ${error}`, 'error')
  } finally {
    loading.value = false
  }
}

const clearResults = () => {
  results.value = []
  log('Results cleared', 'info')
}

// Lifecycle
onMounted(() => {
  initBackend()
  log('Vue Backend Test View loaded', 'info')
  log(`Context: ${context.value}`, 'info')
})
</script>

<style scoped>
.backend-test {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.scene-info, .api-test, .results {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.badges {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.badge.on {
  background: #4caf50;
  color: white;
}

.badge.off {
  background: #f44336;
  color: white;
}

.controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 15px;
}

.name-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 200px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn.primary {
  background: #2196F3;
  color: white;
}

.btn.primary:hover:not(:disabled) {
  background: #1976D2;
}

.btn.secondary {
  background: #757575;
  color: white;
}

.btn.secondary:hover {
  background: #616161;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.backend-switching {
  font-size: 12px;
  color: #666;
}

.backend-switching a {
  color: #2196F3;
  text-decoration: none;
  margin: 0 5px;
}

.backend-switching a:hover {
  text-decoration: underline;
}

.results-container {
  background: #000;
  color: #00ff00;
  padding: 15px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  height: 300px;
  overflow-y: auto;
  line-height: 1.4;
}

.result-item {
  margin-bottom: 5px;
}

.result-item.success {
  color: #4caf50;
}

.result-item.error {
  color: #f44336;
}

.result-item.info {
  color: #2196F3;
}

.timestamp {
  color: #888;
  margin-right: 10px;
}
</style>
