# Graphium Sarpedon

<hr>

# Graphium Sarpedon: Portable Studio

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

<hr>

# Graphium Sarpedon: the Notes

**here goes the devlog**
* the 25th of july
  the main idea of the app was the portable web version which i could easily create as fronted dev, but it is time for grow bigger

  i decided to code app in way of devices: win, macos, linux
  so now i need .exe build and still need portable version for macos and linux because i dont have macos laptop now for proper coding
  for mobile device in the future ill have an .apk build

  so the .exe build bases on c++ vs c# choice, right?
  "for an app tailored for graphics tablets on Windows, C# is overwhelmingly the better choice for almost every developer"
  well, for now ill try cpp

  15:25 did try raylib. well, this is funny, but over pixellery
  <img width="402" height="319" alt="screen-record-1784982316595" src="https://github.com/user-attachments/assets/c9e27741-a2e9-43a7-980c-7da6d688a170" /> <br>

  16:24 came up with open gl
  <img width="789" height="540" alt="screen-record-1784985877514" src="https://github.com/user-attachments/assets/b92d79f8-6e67-44fb-8234-99a2d523f607" /> <br>

  16:37 well as a web developer i can officially say that "growing" can wait and ill try make .exe of graphium via tauri. enough cpp for me, sorry
* the 27th of july
  working now on the idea of the "nodes" for graphium. learning stuff about pop-up windows, thinking on api's work and how to base local server (python vs nodejs, why not both?)

* the 29th of july
  congrats! now i have a vector-paint! so basically its the main thing. now i need to make a million pannels in visual studio code's style <br>
  <img width="1280" height="530" alt="image" src="https://github.com/user-attachments/assets/89aaf2c8-89fb-4fad-a670-e46e1cb9e095" />

* the 2nd of august
  gosh i love portable version so much, still need to fix it on mobile and do optimization for cheap laptops. its definitely gonna be pretty funny to UNprivate this repo when it will be time for release version  
* the 8th of august
  preparing a lot of update stuff for graphium, didnt complete them in the week before cuz of busy timeline
* the 9th of august
  preparing design, animations, pdf export and latex support + vector stylus notes into pages with LaTeX automatically
* the 10th of august
  fixing bugs, a ton of updates: LaTeX, pdf support; new menu and navigation, custom svg icons
