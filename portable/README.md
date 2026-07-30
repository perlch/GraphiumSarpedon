# Vector Canvas Studio

An infinite SVG canvas and vector note-taking web application designed for styluses and graphic tablets, powered by a local Python backend server with multi-window synchronization support.

## Features

* Infinite SVG Canvas: Smooth drawing, panning, and zooming with support for brushes, lines, circles, erasers, shape fills, color pickers, and text insertion.
* Vector Transformation: Select, move, scale, and rotate drawn elements with visual boundary boxes and transformation handles.
* Multi-Window Sync: Uses the `BroadcastChannel` API to synchronize tools, colors, history states, and workspace content in real-time across multiple browser windows (e.g., pop-out toolbars or file managers).
* Local File Management & Server: A Python-based HTTP server built with `tkinter` GUI control panel that lets you manage files and folders safely in a local `memory` directory.
* Import & Export: Export your workspace as an SVG or PNG image, import existing SVG files, or paste images directly from the clipboard.

## Project Structure

* `vecmyself.html` — The main frontend application containing the infinite canvas interface, tools, and multi-window communication logic.
* `server.py` — The Python backend server (`tkinter` + `http.server`) managing file operations (tree navigation, reading, writing, renaming, and deleting SVG files) with CORS enabled.

## Requirements

* Python 3.x (Standard library modules only: `os`, `json`, `http.server`, `socketserver`, `threading`, `urllib`, `shutil`, `base64`, `tkinter`)
* Any modern web browser supporting HTML5, SVG, and BroadcastChannel API.

## Getting Started

1. Run the Python backend server:
   ```bash
   python server.py
2. Open the app.html

   You can use the graphium without server too, with exporting and importing svg/png files
