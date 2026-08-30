# Windows Build

This folder does not contain a separate codebase. The application code here is exactly the same as the browser version in the `web` directory — nothing about the interface, tools, or storage format differs.

This build simply wraps that same web app into a native Windows executable using [Tauri](https://tauri.app/), so it can be installed and launched like a regular desktop app instead of being opened manually in a browser.

A ready-to-download `.exe` is available on the project's **Releases** page — building it yourself from this folder is only necessary if you want to modify the packaging.
