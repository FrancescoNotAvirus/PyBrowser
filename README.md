# PyBrowser

A minimalist tabbed web browser built with PyQt5 and the QtWebEngine.

This is a lightweight navigation tool designed to force a stripped-back web experience. It uses a legacy User-Agent and specific query parameters to trigger "low-end" versions of modern websites, significantly reducing resource consumption.

## Technical Details

### Web Engine
The browser uses QWebEngineView, a Chromium-based rendering engine. This provides full support for modern web standards while allowing for low-level manipulation of browser headers and profiles.

### Resource Optimization
To maintain a low memory footprint, the browser implements several specific configurations:
- User-Agent Spoofing: Identifies as Chrome 100 on Windows 6.1. This forces sites like Google to serve minimalist HTML versions rather than heavy, script-laden modern versions.
- Search Parameters: The default home URL uses the `igu=1` parameter to ensure the search interface remains in its most basic, high-speed state.
- Document Mode: The UI uses QTabWidget in document mode to reduce window chrome and focus purely on the web content.

### Logic Flow
1. Initialization: The main window sets up a QWebEngineProfile with a customized global User-Agent.
2. Tab Management: A BrowserTab class wraps each QWebEngineView instance, handling individual zoom levels and layout margins.
3. URL Handling: The address bar includes a sanitize function that checks for the "http" prefix. If missing, it automatically prepends "https://" before passing the string to the QUrl constructor.
4. Navigation Sync: Signal-slot connections ensure the URL bar updates in real-time as the user navigates through different tabs or follows links within a page.

## Requirements
- Python 3.x
- PyQt5
- PyQtWebEngine

## Installation and Execution

1. Install the required libraries via pip:
   pip install PyQt5 PyQtWebEngine

2. Run the script:
   python browser_pybrowser.py



## License
MIT
