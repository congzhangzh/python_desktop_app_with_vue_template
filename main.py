#!/usr/bin/env python3
"""
Main Application - Core business logic in one place
"""
import os
import socket
import threading
import http.server
import socketserver
from webview_abstraction import create_webview


def is_dev_server_running():
    """Check if dev server is running"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 5173))
    sock.close()
    return result == 0


def start_http_server(directory, port=8000):
    """Start HTTP server for static files"""
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"🌐 Server at http://localhost:{port}")
        httpd.serve_forever()


def get_frontend_url():
    """Get frontend URL - core business logic here"""
    # 1. Check dev server
    if is_dev_server_running():
        print("✅ Dev server")
        return "http://localhost:5173"
    
    # 2. Check dist folder
    if os.path.exists("frontend/dist"):
        print("✅ Using dist + http.server")
        threading.Thread(target=start_http_server, args=("frontend/dist", 8000), daemon=True).start()
        return "http://localhost:8000"
    
    # 3. Fallback
    print("⚠️ No frontend")
    return "data:text/html,<h1>Vue Desktop App</h1><p>No Vue frontend found</p><p>Run: npm run dev</p>"


def add_business_features(webview):
    """Add your business features here"""
    # TODO: Add API bindings
    # TODO: Add database connections  
    # TODO: Add business logic handlers
    pass


def main(webview_type='webview_python'):
    """Main application entry point"""
    print(f"🚀 Starting Vue Desktop App with {webview_type}...")
    
    try:
        # Create webview (only this part is abstracted)
        webview = create_webview(webview_type)
        webview.set_title("Vue Desktop App")
        
        # Core business logic (all in one place, easy to modify)
        frontend_url = get_frontend_url()
        add_business_features(webview)
        
        # Run app
        webview.navigate(frontend_url)
        webview.run()
        
    except ImportError as e:
        print(f"❌ Failed to create {webview_type}: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    # Easy switching: python app.py webview_python|webui|qt4
    webview_type = sys.argv[1] if len(sys.argv) > 1 else 'webview_python'
    main(webview_type)
