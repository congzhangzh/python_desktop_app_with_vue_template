#!/usr/bin/env python3
"""
Main Application - Core business logic in one place
"""
import os
import socket
import pathlib
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

def _get_port():
    """Get a usable port for http.server"""
    # TODO: how to get a usable port for http.server?
    return 8000

def _get_fe_backend_type():
    context = os.getenv("PDV_FE_DATA_BACKEND_TYPE")
    return context if context else "mock"

def get_frontend_url():
    """Get frontend URL - core business logic here"""
    if os.getenv("PDV_FE_BE_CONCEPT_DEBUG") == "true":
        print("✅ Using frontend-dummy + http.server")
        frontend_dummy_dir = pathlib.Path(__file__).parent / "frontend-dummy"
        threading.Thread(
            target=start_http_server, 
            args=(frontend_dummy_dir, _get_port()), 
            daemon=True
        ).start()
        return "http://localhost:8000"
    # 1. Check dev server
    if is_dev_server_running():
        print("✅ Dev server")
        return "http://localhost:5173"
    
    # 2. Check dist folder
    if os.path.exists("frontend/dist"):
        print("✅ Using dist + http.server")
        threading.Thread(
            target=start_http_server, 
            args=("frontend/dist", _get_port()), 
            daemon=True
        ).start()
        return "http://localhost:8000"
    
    # 3. Fallback
    print("⚠️ No frontend")
    return ("data:text/html,<h1>Vue Desktop App</h1><p>No Vue frontend found</p>"
            "<p>Run: npm run dev</p>")


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
        fe_backend_type = _get_fe_backend_type()
        add_business_features(webview)
        
        # Run app
        webview.navigate(rf'{frontend_url}#backend_type={fe_backend_type}')
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
