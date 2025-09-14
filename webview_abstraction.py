#!/usr/bin/env python3
"""
WebView Abstraction - Only abstract the webview part
"""
from abc import ABC, abstractmethod


class WebViewInterface(ABC):
    """Abstract WebView interface"""
    
    @abstractmethod
    def set_title(self, title: str):
        """Set window title"""
        pass
    
    @abstractmethod
    def navigate(self, url: str):
        """Navigate to URL"""
        pass
    
    @abstractmethod
    def run(self):
        """Start the webview"""
        pass


class WebViewPythonAdapter(WebViewInterface):
    """webview_python implementation"""
    
    def __init__(self):
        from webview.webview import Webview
        self.webview = Webview()
    
    def set_title(self, title: str):
        self.webview.title = title
    
    def navigate(self, url: str):
        self.webview.navigate(url)
    
    def run(self):
        self.webview.run()


class WebUIAdapter(WebViewInterface):
    """WebUI implementation"""
    
    def __init__(self):
        from webui import webui
        self.window = webui.new_window()
        self.webui = webui
    
    def set_title(self, title: str):
        # WebUI sets title automatically
        pass
    
    def navigate(self, url: str):
        self.webui.show(self.window, url)
    
    def run(self):
        self.webui.wait()


class Qt4WebViewAdapter(WebViewInterface):
    """Qt4 WebView implementation"""
    
    def __init__(self):
        import sys
        from PyQt4 import QtCore, QtGui, QtWebKit
        
        self.app = QtGui.QApplication(sys.argv)
        self.window = QtGui.QMainWindow()
        self.window.setGeometry(100, 100, 1200, 800)
        
        self.webview = QtWebKit.QWebView(self.window)
        self.window.setCentralWidget(self.webview)
        
        self.QtCore = QtCore
        self.sys = sys
    
    def set_title(self, title: str):
        self.window.setWindowTitle(title)
    
    def navigate(self, url: str):
        self.webview.load(self.QtCore.QUrl(url))
    
    def run(self):
        self.window.show()
        self.sys.exit(self.app.exec_())


def create_webview(webview_type='webview_python'):
    """Create webview instance by type"""
    adapters = {
        'webview_python': WebViewPythonAdapter,
        'webui': WebUIAdapter, 
        'qt4': Qt4WebViewAdapter,
    }
    
    if webview_type not in adapters:
        raise ValueError(f"Unknown webview type: {webview_type}")
    
    try:
        return adapters[webview_type]()
    except ImportError as e:
        raise ImportError(f"Failed to import {webview_type}: {e}") from e
