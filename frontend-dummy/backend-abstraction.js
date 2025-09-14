/**
 * Backend Abstraction Layer
 * Provides unified interface for different backend integrations
 */

// Context information from backend
const getContext = () => {
  // Check URL hash for backend_type (e.g., #backend_type=webview)
  const hash = window.location.hash
  const hashMatch = hash.match(/backend_type=(\w+)/)
  return hashMatch?hashMatch[1]:'mock'
}

// Debug logger - only when debug mode is enabled
const log = (...args) => {
  if (FE_BE_CONCEPT_DEBUG) {
    console.log('[Backend API]', ...args)
  }
}

// Always log important info
const info = (...args) => {
  console.log('[Backend API]', ...args)
}

/**
 * Abstract Backend Interface - Simplified
 */
class BackendInterface {
  async say_hello(name) { throw new Error('Not implemented') }
  async say_hello_async(name) { throw new Error('Not implemented') }
}

/**
 * Mock Backend Implementation
 */
class MockBackend extends BackendInterface {
  async say_hello(name) {
    log('Mock: say_hello()', name)
    await this._simulateDelay()
    return `Hello ${name}! (from Mock Backend)`
  }
  
  async say_hello_async(name) {
    log('Mock: say_hello_async()', name)
    await this._simulateDelay(500, 1500) // Longer delay for async demo
    return `Hello ${name}! (from Mock Backend - Async)`
  }
  
  async _simulateDelay(min = 100, max = 500) {
    const delay = Math.random() * (max - min) + min
    await new Promise(resolve => setTimeout(resolve, delay))
  }
}

/**
 * WebView Python Binding Backend
 */
class WebViewPythonBackend extends BackendInterface {
  async say_hello(name) {
    log('WebViewPython: say_hello()', name)
    try {
      if (window.pywebview && window.pywebview.api) {
        return await window.pywebview.api.say_hello(name)
      }
      throw new Error('PyWebView API not available')
    } catch (error) {
      log('Error:', error)
      throw error
    }
  }
  
  async say_hello_async(name) {
    log('WebViewPython: say_hello_async()', name)
    try {
      if (window.pywebview && window.pywebview.api) {
        return await window.pywebview.api.say_hello_async(name)
      }
      throw new Error('PyWebView API not available')
    } catch (error) {
      log('Error:', error)
      throw error
    }
  }
}

/**
 * WebUI Backend Implementation
 */
class WebUIBackend extends BackendInterface {
  async say_hello(name) {
    log('WebUI: say_hello()', name)
    try {
      if (window.webui) {
        return await window.webui.call('say_hello', name)
      }
      throw new Error('WebUI not available')
    } catch (error) {
      log('Error:', error)
      throw error
    }
  }
  
  async say_hello_async(name) {
    log('WebUI: say_hello_async()', name)
    try {
      if (window.webui) {
        return await window.webui.call('say_hello_async', name)
      }
      throw new Error('WebUI not available')
    } catch (error) {
      log('Error:', error)
      throw error
    }
  }
}

/**
 * Qt4 WebView Backend (simplified for demo)
 */
class Qt4Backend extends BackendInterface {
  async say_hello(name) {
    log('Qt4: say_hello()', name)
    // Qt4 would typically use Qt bridge or custom JS injection
    return `Hello ${name}! (from Qt4 Backend)`
  }
  
  async say_hello_async(name) {
    log('Qt4: say_hello_async()', name)
    // Simulate async with delay
    await new Promise(resolve => setTimeout(resolve, 800))
    return `Hello ${name}! (from Qt4 Backend - Async)`
  }
}

/**
 * Backend Factory
 */
class BackendFactory {
  static create() {
    const context = getContext()
   
    info(`Expected backend type from scene: ${context}`)
    
    // Force backend type from hash (e.g., #backend_type=mock)
    if (context === 'mock') {
      info('Using Mock Backend (forced by URL hash)')
      return new MockBackend()
    }
    if (context === 'webview') {
      info('Using WebView Backend (forced by URL hash)')
      return new WebViewPythonBackend()
    }
    if (context === 'webui') {
      info('Using WebUI Backend (forced by URL hash)')
      return new WebUIBackend()
    }
    if (context === 'qt') {
      info('Using Qt4 Backend (forced by URL hash)')
      return new Qt4Backend()
    }
    
    throw new Error(`Unknown backend type: ${context}`)
  }
}

// Export
export {
  BackendInterface,
  BackendFactory
}