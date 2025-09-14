#!/usr/bin/env python3
"""
Main Application - Core business logic in one place
"""
import os
import sys
import pathlib
import threading
import http.server
import socketserver
import urllib.request
import urllib.error
import logging
import datetime
from webview_abstraction import create_webview
import faulthandler

def is_frozen():
    """Check if the application is frozen"""
    return getattr(sys, 'frozen', False)

def is_windowed_mode():
    """更简单的检测方法"""
    import io
    # 如果stdout被重定向或不存在，说明是窗口模式
    return not hasattr(sys.stdout, 'write') or isinstance(sys.stdout, io.StringIO)

if is_windowed_mode():
    # Or http.server will do nothing, even hold the port but not serve the files and raise no exception
    sys.stdout = sys.stderr = open('stdout.log', 'w', encoding='utf-8')

if not is_windowed_mode():
    faulthandler.enable()

def setup_logging():
    """Setup logging for both development and frozen environment"""
    if is_frozen():
        # In frozen app, log to file next to exe
        log_dir = os.path.dirname(sys.executable)
        log_file = os.path.join(log_dir, "app.log")
    else:
        # In development, log to project directory
        log_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(log_dir, "app.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)  # Still show in console for development
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"🚀 Application started, frozen: {is_frozen()}")
    logger.info(f"📝 Log file: {log_file}")
    return logger

def is_dev_server_running():
    """Check if dev server is running"""
    logger = logging.getLogger(__name__)
    try:
        # Try to make HTTP request to dev server
        response = urllib.request.urlopen('http://localhost:5173', timeout=3)
        is_running = response.status == 200
        logger.info(f"🌐 Dev server is running: {is_running}, status: {response.status}")
        return is_running
    except urllib.error.URLError as e:
        logger.info(f"🌐 Dev server is not running: {e}")
        return False
    except Exception as e:
        logger.error(f"🌐 Exception checking dev server: {e}")
        return False

def start_http_server(directory, port_callback=None, ready_event=None):
    """Start HTTP server and signal when ready"""
    try:
        logger = logging.getLogger(__name__)
        logger.info(f"🌐 Starting HTTP server for static files in {directory}")
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=directory, **kwargs)
        
        # Let TCPServer choose the port to avoid race conditions
        with socketserver.TCPServer(("", 0), Handler) as httpd:
            actual_port = httpd.server_address[1]
            logger.info(f"🌐 Server started at http://localhost:{actual_port}")
            
            # Notify the caller of the actual port
            if port_callback:
                port_callback(actual_port)
            
            # Signal that server is ready
            if ready_event:
                ready_event.set()
            
            httpd.serve_forever()
        logger.info(f"🌐 Server stopped")
    except Exception as e:
        logger.error(f"🌐 Exception starting http server: {e}")
        if ready_event:
            ready_event.set()  # Signal even on error
        raise e


def _get_fe_backend_type():
    context = os.getenv("PDV_FE_DATA_BACKEND_TYPE")
    return context if context else "mock"

def get_frontend_url():
    """Get frontend URL - core business logic here"""
    logger = logging.getLogger(__name__)
    
    if is_frozen():
        logger.info(f"🌐 Running as frozen app, sys.executable: {sys.executable}")
        dist_path = pathlib.Path(sys.executable).parent /"_internal"/"frontend" / "dist"
        if not dist_path.exists():
            logger.error(f"🌐 Dist path does not exist: {dist_path}")
            raise FileNotFoundError(f"Dist path does not exist: {dist_path}")
        logger.info(f"✅ Using dist + http.server, path: {dist_path}")
        
        # Use Event for proper synchronization
        actual_port = {'port': None}
        ready_event = threading.Event()
        
        def port_callback(port):
            actual_port['port'] = port
        
        threading.Thread(
            target=start_http_server, 
            args=(str(dist_path),), 
            kwargs={'port_callback': port_callback, 'ready_event': ready_event},
            daemon=True
        ).start()
        
        # Wait for server to be ready (max 10 seconds)
        if not ready_event.wait(timeout=10):
            raise RuntimeError("HTTP server failed to start within 10 seconds")
        
        if actual_port['port'] is None:
            raise RuntimeError("HTTP server failed to start")
            
        logger.info(f"🌐 HTTP server ready on port {actual_port['port']}")
        return f"http://localhost:{actual_port['port']}"
    elif os.getenv("PDV_FE_BE_CONCEPT_DEBUG") == "true":
        logger.info("✅ Using frontend-dummy + http.server")
        frontend_dummy_dir = pathlib.Path(__file__).parent / "frontend-dummy"
        # Use the same Event-based mechanism for consistency
        actual_port = {'port': None}
        ready_event = threading.Event()
        
        def port_callback(port):
            actual_port['port'] = port
        
        threading.Thread(
            target=start_http_server, 
            args=(str(frontend_dummy_dir),), 
            kwargs={'port_callback': port_callback, 'ready_event': ready_event},
            daemon=True
        ).start()
        
        # Wait for server to be ready
        if not ready_event.wait(timeout=10):
            raise RuntimeError("Debug HTTP server failed to start")
            
        return f"http://localhost:{actual_port['port']}"
    # 1. Check dev server
    elif is_dev_server_running():
        logger.info("✅ Dev server")
        return "http://localhost:5173"
    
    # 3. Fallback
    logger.warning("⚠️ No frontend")
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
    # Setup logging first
    logger = setup_logging()
    logger.info(f"🚀 Starting Vue Desktop App with {webview_type}...")
    
    try:
        # Create webview (only this part is abstracted)
        webview = create_webview(webview_type)
        webview.set_title("Vue Desktop App")
        
        # Core business logic (all in one place, easy to modify)
        frontend_url = get_frontend_url()
        fe_backend_type = _get_fe_backend_type()
        logger.info(f"🌐 Frontend URL: {frontend_url}")
        logger.info(f"🔧 Backend type: {fe_backend_type}")
        add_business_features(webview)
        
        # Run app
        webview.navigate(rf'{frontend_url}#backend_type={fe_backend_type}')
        webview.run()
        
    except ImportError as e:
        logger.error(f"❌ Failed to create {webview_type}: {e}")
        raise e
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise e


if __name__ == "__main__":
    import sys
    # import os
    # os.environ["WEBVIEW2_USER_DATA_FOLDER"]="your_cache_dir"
    # os.environ["WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS"]= " --remote-debugging-port=9222 --remote-allow-origins=*"
    # Easy switching: python app.py webview_python|webui|qt4
    webview_type = sys.argv[1] if len(sys.argv) > 1 else 'webview_python'
    main(webview_type)
