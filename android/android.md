# Android Build

This folder does not contain a separate codebase. The application code here is exactly the same as the browser version in the `web` directory — nothing about the interface, tools, or storage format differs.

This build simply wraps that same web app into a native Android package using [Apache Cordova](https://cordova.apache.org/), so it can be installed and launched like a regular mobile app instead of being opened manually in a browser.

A ready-to-download `.apk` is available on the project's **Releases** page — building it yourself from this folder is only necessary if you want to modify the packaging. <br>
<hr>
**Personal recommendation:** Use Termux to run the server on Android.
