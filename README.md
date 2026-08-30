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

* `index.html` — The main frontend application containing the infinite canvas interface, tools, and multi-window communication logic.
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
  [18:35] some test
* the 11th of august
  there are actually a big amount of fixes and more-stuff to add in graphium right now afte my few updates. as a "dev diary" i should add some screens, so there goes a few screens of 0.0.3 version of graphium i called "Deltote deceptoria": <br>
  <img width="1024" height="768" alt="image" src="https://github.com/user-attachments/assets/a3890bd0-c666-4f05-b5a9-b143de790e7c" /> <br>
  <img width="960" height="434" alt="image" src="https://github.com/user-attachments/assets/d742ca8c-ea39-4d51-8b12-08b258860f2c" /> <br>
  <img width="960" height="435" alt="image" src="https://github.com/user-attachments/assets/e0f94f5c-e0d9-49d0-b8f2-a9a5cab631c6" /> <br>
  <img width="960" height="435" alt="image" src="https://github.com/user-attachments/assets/e7e81435-f924-4b15-a2aa-baa625de9840" /> <br>
  [16:22] holy shi in future ill have to make good README pls no :sob:
* the 12th of august
  <img width="482" height="447" alt="image" src="https://github.com/user-attachments/assets/238ee308-6c1d-41a3-bac3-823fd379e441" />
* the 13th of august
  so i need to do a big amount of notes today thats why im updtaing graphium hard today. btw i'll need to remove this diary somewhere else from maind readme, the commit's story would be fun to read <br> <img width="942" height="436" alt="image" src="https://github.com/user-attachments/assets/9bf5fdee-efc8-4b40-8fd3-af0c4c5b3537" />
* the 14th of august
  naming my app in the name of butterflies was the COOLest idea <br>
  <img width="424" height="321" alt="image" src="https://github.com/user-attachments/assets/efff7a02-e483-4a98-8d20-f45cc9613055" /> <br>
  so, im actually still need to fix that bug with moving of pictures. also im not sure about pdf export of slides, but i still belive it would be cool to convert hand-text to type-text
* the 22nd of august
  preparing the v1.0.0 version of graphium, did a lot of work, cleared trash and added classes (instead of functions spam), preparing place for future api stuff and fixing instruments; working fast on logo, thinking of documentation and migration of graphium-dev diary. working hard, notes are great
  [12:37] so there is a lot of new stuff, i killed all of the latex for maybe feature updates/libs/apps and instead add the second instuments bar with figures, calc and math builder. pretty neat feature and actually dope for notes! okay that's all of the blablabla now, after finishing the code of 1.0.0i have to create a main web page for it and also good doc. aargh 
* the 23rd of august
  <img width="1280" height="579" alt="image" src="https://github.com/user-attachments/assets/f767dffb-d1c5-4d9f-a41e-8f2ef21b6fe9" />
* the 24oth of august
  developed logo <br>
  <img width="730" height="718" alt="image" src="https://github.com/user-attachments/assets/86f14267-a047-41c7-a53c-3fda617fc338" />
* the 27th of august
  today is a day - building first versions, .exe, .apk, moving devlog somewhere else probably to trash 
* the 28th of august
  first .exe build is done.
  [12:41] graphium sarpedon, windows 11 <br>
  <img width="313" height="250" alt="image" src="https://github.com/user-attachments/assets/74ccf595-944f-47b8-a912-b669b4d58d9b" />
* the 30th of august
  i did the .apk build, i did docs, now i need to structure all of that and make cool intro webpage. im really love that its gonna perfectly hit the start of autumn 
