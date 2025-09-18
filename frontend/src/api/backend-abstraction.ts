/**
 * Vue Frontend Backend Abstraction
 * 与 frontend-dummy/backend-abstraction.js 保持API一致
 */

// Context information from backend
const getContext = (): string => {
  // Check URL hash for backend_type (e.g., #backend_type=webview)
  // TODO query string is a better way?
  const hash = window.location.hash
  const hashMatch = hash.match(/backend_type=(\w+)/)
  return hashMatch ? hashMatch[1] : 'mock'
}

// Debug logger
const log = (...args: any[]) => {
  console.log('[Vue Backend API]', ...args)
}

// Always log important info
const info = (...args: any[]) => {
  console.log('[Vue Backend API]', ...args)
}

/**
 * Abstract Backend Interface - Simplified
 */
export class BackendInterface {
  public context: string = 'unknown'
  
  async say_hello(name: string): Promise<string> { 
    throw new Error('Not implemented') 
  }
  async say_hello_async(name: string): Promise<string> { 
    throw new Error('Not implemented') 
  }
}

/**
 * Mock Backend Implementation
 */
export class MockBackend extends BackendInterface {
  async say_hello(name: string): Promise<string> {
    log('Mock: say_hello()', name)
    await this._simulateDelay()
    return `Hello ${name}! (from Mock Backend)`
  }
  
  async say_hello_async(name: string): Promise<string> {
    log('Mock: say_hello_async()', name)
    await this._simulateDelay(500, 1500) // Longer delay for async demo
    return `Hello ${name}! (from Mock Backend - Async)`
  }
  
  async _simulateDelay(min = 100, max = 500): Promise<void> {
    const delay = Math.random() * (max - min) + min
    await new Promise(resolve => setTimeout(resolve, delay))
  }
}

/**
 * WebView Python Binding Backend
 */
export class WebViewPythonBackend extends BackendInterface {
  async say_hello(name: string): Promise<string> {
    log('WebViewPython: say_hello()', name)
    try {
      if ((window as any).pywebview && (window as any).pywebview.api) {
        return await (window as any).pywebview.api.say_hello(name)
      }
      throw new Error('PyWebView API not available')
    } catch (error) {
      log('Error:', error)
      throw error
    }
  }
  
  async say_hello_async(name: string): Promise<string> {
    log('WebViewPython: say_hello_async()', name)
    try {
      if ((window as any).pywebview && (window as any).pywebview.api) {
        return await (window as any).pywebview.api.say_hello_async(name)
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
export class WebUIBackend extends BackendInterface {
  async say_hello(name: string): Promise<string> {
    log('WebUI: say_hello()', name)
    try {
      if ((window as any).webui) {
        return await (window as any).webui.call('say_hello', name)
      }
      throw new Error('WebUI not available')
    } catch (error) {
      log('Error:', error)
      throw error
    }
  }
  
  async say_hello_async(name: string): Promise<string> {
    log('WebUI: say_hello_async()', name)
    try {
      if ((window as any).webui) {
        return await (window as any).webui.call('say_hello_async', name)
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
export class Qt4Backend extends BackendInterface {
  async say_hello(name: string): Promise<string> {
    log('Qt4: say_hello()', name)
    // Qt4 would typically use Qt bridge or custom JS injection
    return `Hello ${name}! (from Qt4 Backend)`
  }
  
  async say_hello_async(name: string): Promise<string> {
    log('Qt4: say_hello_async()', name)
    // Simulate async with delay
    await new Promise(resolve => setTimeout(resolve, 800))
    return `Hello ${name}! (from Qt4 Backend - Async)`
  }
}

/**
 * Backend Factory
 */
export class BackendFactory {
  static create(): BackendInterface {
    const context = getContext()
   
    info(`Expected backend type from scene: ${context}`)
    
    let backend: BackendInterface
    
    // Force backend type from hash (e.g., #backend_type=mock)
    if (context === 'mock') {
      info('Using Mock Backend (forced by URL hash)')
      backend = new MockBackend()
    } else if (context === 'webview') {
      info('Using WebView Backend (forced by URL hash)')
      backend = new WebViewPythonBackend()
    } else if (context === 'webui') {
      info('Using WebUI Backend (forced by URL hash)')
      backend = new WebUIBackend()
    } else if (context === 'qt') {
      info('Using Qt4 Backend (forced by URL hash)')
      backend = new Qt4Backend()
    } else {
      throw new Error(`Unknown backend type: ${context}`)
    }
    
    // Factory 负责设置 context
    backend.context = context
    return backend
  }
}

// Export convenience function
export const createBackend = () => BackendFactory.create()
