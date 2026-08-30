<div align="center">
  <img width="343" height="321" alt="graphium_dark" src="https://github.com/user-attachments/assets/13fa6115-9c68-4ab0-b236-140eaf54d4f3" />
  <br>
  <em>Graphium Sarpedon</em>
</div>

# Graphium Sarpedon

Graphium is a browser-based vector note-taking application designed for stylus and graphics-tablet input. It is implemented as a single, self-contained HTML document on the client side, paired with a minimal Python backend that persists notes as native SVG files on the user's own filesystem.

## 1. Relevance of the Work

The past several years have seen a marked shift in how technical notes, diagrams, and handwritten mathematics are produced: tablets, 2-in-1 laptops, and stylus-enabled displays are now common tools in both education and professional engineering work. This shift has exposed a gap in the tooling available for digital note-taking. Most widely used applications render ink as a raster bitmap on a canvas surface, which means that content loses sharpness when zoomed, scales poorly across displays of different pixel density, and is difficult to edit non-destructively after the fact.

At the same time, the amount of technical content that mixes freehand diagrams with formal mathematical work continues to grow, particularly in STEM education and exam preparation, where a single note may combine a hand-drawn sketch, a labelled diagram, and a quick calculation or plotted graph. Very few lightweight tools address this combination directly, and fewer still do so while keeping the underlying data in an open, inspectable, vector format rather than a proprietary or cloud-locked one. Graphium was developed to address this specific intersection: resolution-independent vector ink, a built-in calculator and function-graph builder, native SVG and PNG import/export, and local-first storage — all delivered through an interaction pipeline optimized enough to keep large, SVG-dense notes comfortable to pan, zoom, and edit, without a mandatory build step or external runtime dependency.

## 2. Rationale for the Choice of Topic

The choice of this topic follows directly from a practical need encountered during personal note-taking with a graphics tablet: existing raster-based whiteboard and note applications were unsatisfactory for long-form technical notes that are revisited, zoomed, and edited repeatedly over time, while existing vector-capable tools were either heavyweight desktop applications with steep learning curves or cloud services that store content in a closed format.

Rather than adapting an existing raster canvas application, the decision was made to design a dedicated tool from first principles, built strictly on the SVG document object model rather than on `<canvas>` pixel manipulation. This decision shaped nearly every subsequent design choice in the project: every stroke, shape, imported image, and piece of text is a real SVG node that can be selected, transformed, and exported without any loss of quality, and the entire application remains a single portable HTML file that can be opened directly in a browser with no installation process.

## 3. Problem Statement

The project addresses the following concrete shortcomings observed in existing note-taking and whiteboard software:

- Canvas-based (raster) drawing surfaces lose visual fidelity when the user zooms in, and any transformation applied after the fact (moving, scaling, or rotating a stroke) is either unsupported or destructive.
- Tools that do offer true vector editing are frequently full desktop suites or browser services with a proprietary save format, offline-storage restrictions, or subscription requirements, which is disproportionate for the comparatively narrow use case of stylus note-taking.
- Quick mathematical work — evaluating an expression or plotting a function — rarely fits inside a drawing surface: most tools require switching to a separate calculator or graphing application, breaking the flow of note-taking.
- Setting up local, self-hosted storage for a browser-based tool typically requires configuring a general-purpose backend stack, even though the underlying requirement is limited to reading, writing, renaming, and deleting a small tree of files.
- Selection and transform tools in many lightweight vector editors are prone to a specific and easily overlooked class of bugs, in which moving an object and then scaling or rotating it (or performing the two in the opposite order) silently discards one of the two operations, because the underlying transform matrix is rebuilt from scratch on each interaction rather than composed consistently.

## 4. Goal of the Work

The goal of the work is to design and implement Graphium, a self-contained, dependency-light, vector-native note-taking application for stylus and graphics-tablet input, offering a complete freehand and geometric drawing toolset, a built-in calculator and function-graph builder, native SVG and PNG import and export, a robust object selection and transform system, and local file persistence through a lightweight companion server, without relying on any canvas rasterization or external frontend framework.

## 5. Objectives of the Work

To achieve the stated goal, the following objectives were defined and pursued:

- Design and implement a purely vector-based (SVG) drawing engine, including a freehand pen, a straight-line tool with snapping to horizontal, vertical, and diagonal angles, an eraser, and an area-fill tool.
- Implement a unified object selection and transform system that supports translation, scaling, and rotation for arbitrary vector paths, imported raster images, and grouped multi-object (lasso) selections, with all transformations pivoting strictly around the selected object's own geometric center rather than around the camera viewport.
- Optimize the SVG rendering and interaction pipeline so that notes containing large numbers of vector elements remain smooth to pan, zoom, select, and edit, keeping SVG-native storage convenient in practice and not only in principle.
- Implement full undo and redo history, and vector-native import and export in both SVG and PNG formats, with PNG import behaving identically to a clipboard paste of an image.
- Preserve compatibility with touch and stylus input, including pinch-to-zoom gestures, so that the application remains fully usable on tablet hardware.
- Build a local file-management backend that exposes the user's notes as a browsable tree of files and folders, with support for creating, reading, writing, renaming, and deleting entries, backed by plain SVG files on disk rather than a database or cloud account.
- Extend the base toolset with supplementary instruments — a highlighter/marker, an in-canvas calculator, a set of parametric geometric shape stamps, and a vector function-graph builder — while keeping the codebase a single portable HTML file with no build tooling.
- Package the version 1.0.0 release beyond the default, install-free browser experience, producing a standalone Windows executable (.exe) and an Android application package (.apk) alongside the browser build.
- Identify and correct defects in the selection and transform pipeline, in particular the class of bugs where sequential move and scale/rotate operations overwrite one another, and where the visual thickness of selection outlines incorrectly depends on the current zoom level.

## 6. Frontend Technologies Used

The client is implemented as a single HTML document combining structure, styling, and behavior, with no build step, package manager, or external frontend framework. The following technologies and techniques are used:

- Vanilla JavaScript (ES6+), organized procedurally around a central application state object and a set of DOM manipulation functions, rather than a component framework.
- The native SVG Document Object Model as the sole drawing substrate. Freehand strokes, straight lines, shapes, images, and text are all represented as real SVG elements (`path`, `line`, `rect`, `circle`, `polygon`, `image`, `text`, `foreignObject`, and `g`), which guarantees that every object remains resolution-independent and individually editable.
- The Pointer Events API (`pointerdown`, `pointermove`, `pointerup`) as a unified input layer, allowing mouse, touch, and stylus input to be handled through a single code path, together with dedicated touch-gesture handling for pinch-to-zoom on tablets.
- CSS custom properties for centralized theming, and CSS transitions for the animated interface elements, including the auto-hiding toolbars and the sliding calculator and graph-builder panels.
- Rendering and interaction optimizations tuned specifically for SVG-heavy documents — batched attribute updates and transform recomputation limited to what has actually changed — so that pan, zoom, selection, and transform operations stay smooth even as the number of vector nodes in a note grows.
- A custom recursive-descent arithmetic expression parser, written from scratch without relying on `eval`, shared between the built-in calculator and the vector function-graph builder.
- The Fetch API, used by the client to communicate with the local backend for listing, reading, writing, renaming, and deleting note files.

## 7. Backend Technologies Used

The backend is a small, dependency-free Python application (`server.py`) that serves two purposes: it exposes a local HTTP API for note storage, and it provides a minimal desktop control panel for starting and stopping that server.

- Python 3 standard library only: `http.server` and `socketserver` provide the HTTP server itself, `threading` runs the server on a background daemon thread so that the control panel remains responsive, and `os`, `json`, `shutil`, `base64`, and `urllib.parse` handle filesystem access, serialization, recursive folder removal, and request parsing. No third-party packages are required.
- A subclass of `SimpleHTTPRequestHandler` adds permissive CORS headers to every response (`Access-Control-Allow-Origin`, `-Methods`, `-Headers`) so that the HTML frontend can call the API regardless of how the page itself is served.
- A small REST-style API is exposed under `/api`:
  - `GET /api/tree` returns a JSON tree of the storage folder's files and subfolders.
  - `GET /api/file` returns the contents of a single file, given a relative path.
  - `POST /api/file` creates or overwrites a file. It accepts the content under any of several body keys (`content`, `svg`, or `data`) for frontend flexibility, and transparently decodes Base64 data-URL payloads before writing them to disk.
  - `POST /api/folder` creates a new folder.
  - `PUT /api/rename` renames or moves a file or folder.
  - `DELETE /api/delete` removes a file, or recursively removes a folder.
- All incoming paths are resolved against the configured storage directory and validated so that the resolved absolute path cannot escape that directory, as a basic safeguard against path traversal.
- Tkinter provides a small native desktop GUI on top of the server: a folder picker to choose (or change) the storage location, a single button to start and stop the HTTP server, and a status label reporting the active URL and folder. The server listens on port 8080 by default, and stores notes in a `memory` folder next to the script unless the user selects a different location.
- Version 1.0.0 is distributed in three forms: as the default, install-free browser application requiring no packaging at all; as a standalone Windows executable (`.exe`) that bundles the Python backend and its Tkinter control panel for users who prefer a native desktop launcher; and as an Android application package (`.apk`) that wraps the frontend for tablet and phone use.

## 8. System Operating Principles

Graphium separates cleanly into a stateless rendering client and a local storage service, connected over HTTP.

On the client, all note content lives inside a single pannable and zoomable SVG viewport. Every drawing tool operates by creating or modifying SVG DOM nodes directly, rather than drawing to a raster buffer, which is what allows any element — a pen stroke, an imported image, a geometric shape, or a plotted function — to remain fully vector and losslessly editable after creation.

Object selection and manipulation are handled by a unified transform system. Rather than rebuilding an element's `transform` attribute independently for each interaction, every selectable element stores its own translation, rotation, and scale as a small persistent record. Move operations update only the translation component, and scale/rotate operations update only the rotation and scale components, both against the same record; the final `transform` string is then rebuilt from that single, consistent source of truth. This is also what allows a lasso selection — internally just a temporary group of the enclosed elements — to be moved, scaled, and rotated using exactly the same code path as any single object, and what keeps every scale and rotation pivoting strictly around the selected object's own center, independent of the current camera zoom or pan position.

Because every object remains a real, addressable SVG node rather than a pixel region, the rendering and interaction code paths are specifically tuned to keep this approach practical at scale: attribute updates are batched rather than applied one at a time, selection and transform operations avoid unnecessary DOM rebuilds, and the pan/zoom viewport only recomputes what has actually changed on screen. This optimization is what keeps panning, zooming, and editing responsive even as a note accumulates hundreds of freehand strokes, shapes, and imported images as native, individually editable SVG elements.

For persistence, the frontend communicates with the local Python backend through the REST-style API described above: requesting the current file tree to populate the sidebar explorer, reading a note's SVG source when it is opened, and writing it back on save. Because the backend only deals in plain SVG (and, for imported raster content, Base64-embedded image data) files on the local disk, notes remain portable, human-readable, and independent of any particular version of the application.

## 9. Results and Conclusion

The result of this work is a functioning, self-contained vector note-taking application that meets the objectives set out above: a full freehand and geometric drawing toolset, a built-in calculator and function-graph builder, undo and redo history, SVG and PNG import and export, and stylus- and touch-friendly pan and zoom, all implemented without canvas rasterization and without any external frontend framework or build step.

During development and subsequent testing, a critical defect was identified and corrected in the selection and transform system: the function responsible for drawing the selection outline was inadvertently clearing the current selection as a side effect of its own cleanup step, which meant that no object — regardless of type — could actually be selected, moved, scaled, or rotated. A second, related defect caused move and scale/rotate operations to overwrite one another when performed in sequence, and a third caused the selection outline's stroke width to vary incorrectly with the camera zoom level rather than remaining constant on screen. All three were traced to their root cause and corrected, and the fix was verified against the running application using an automated headless-browser test covering direct object selection, sequential move-then-transform operations, image dragging, and lasso-group rotation.

Beyond the base toolset, the application was extended with a secondary, collapsible toolbar offering an adjustable-width highlighter, an in-canvas calculator backed by a custom expression parser, a set of ten parametric geometric shape stamps, and a vector function-graph builder capable of plotting explicit functions and simple circle equations directly onto the canvas as native, editable SVG geometry. The overall codebase remains a single portable HTML file, and the storage layer remains a minimal, dependency-free local server, in keeping with the project's original design constraints. For version 1.0.0, the application is additionally packaged into two standalone builds — a Windows executable (`.exe`) and an Android application package (`.apk`) — alongside its default, install-free browser build, and the rendering pipeline's optimizations keep even SVG-dense notes comfortable to pan, zoom, and edit across all three.

## 10. Further Development Prospects

Several directions have been identified for future iterations of the project:

- A formal plugin or library interface, allowing third parties to package additional tools, shape sets, or content templates and distribute them independently of the core application, in the spirit of the extension ecosystems found in tools such as Obsidian.
- A gradual, backward-compatible refactor of the client codebase from its current procedural structure toward a modular, class-based architecture, intended to make the above plugin interface practical to implement and maintain as the toolset continues to grow.
- Expansion of the function-graph builder to support parametric and polar equations, and implicit curves beyond the circle case currently handled.
- Inline LaTeX rendering for typeset mathematical notation directly within text elements on the canvas, as a richer, publication-quality complement to the current built-in calculator and function-graph builder.
- Pressure- and tilt-sensitive stroke rendering, using the pressure and tilt properties already available through the Pointer Events API.
- Optional real-time collaborative editing and multi-device synchronization, layered on top of the existing local-first storage model rather than replacing it.
- Organizational features for larger note collections, such as tagging, full-text and formula search across stored notes, and a searchable multi-page or infinite-canvas layout.

<div align="center">
  <img width="1000" height="1000" alt="icon" src="https://github.com/user-attachments/assets/3ba5278e-111d-4c77-b405-8ca4130d90f7" />

  <br>
  <em>Graphium Sarpedon</em>
</div>
