import os
import json
import http.server
import socketserver
import threading
import urllib.parse
import shutil
import base64
import tkinter as tk
from tkinter import filedialog, messagebox

server_thread = None
httpd = None
is_running = False
PORT = 8080

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory")

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE, PUT')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def get_safe_path(self, req_path):
        clean_path = req_path.lstrip('/').replace('\\', '/')
        full_path = os.path.abspath(os.path.join(BASE_DIR, clean_path))
        if not full_path.startswith(BASE_DIR):
            raise ValueError("Invalid path access")
        return full_path

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8')) if post_data else {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == '/api/tree':
            if not os.path.exists(BASE_DIR):
                os.makedirs(BASE_DIR, exist_ok=True)
            tree = self.build_tree(BASE_DIR)
            self._send_json(tree)
        elif path == '/api/file':
            try:
                rel_path = query.get('path', [''])[0]
                full_path = self.get_safe_path(rel_path)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._send_json({"data": content})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        try:
            body = self._read_body()
            rel_path = body.get('path', '')
            full_path = self.get_safe_path(rel_path)
            
            if path == '/api/file':
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                content = body.get('content') or body.get('svg') or body.get('data') or ''
                
                if isinstance(content, str) and 'base64,' in content:
                    try:
                        header, encoded = content.split('base64,', 1)
                        content = base64.b64decode(encoded).decode('utf-8')
                    except Exception:
                        pass

                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                self._send_json({"status": "ok"})
                
            elif path == '/api/folder':
                os.makedirs(full_path, exist_ok=True)
                self._send_json({"status": "ok"})
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/rename':
            try:
                body = self._read_body()
                old_path = self.get_safe_path(body.get('old', ''))
                new_path = self.get_safe_path(body.get('new', ''))
                os.rename(old_path, new_path)
                self._send_json({"status": "ok"})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == '/api/delete':
            try:
                rel_path = query.get('path', [''])[0]
                full_path = self.get_safe_path(rel_path)
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                else:
                    os.remove(full_path)
                self._send_json({"status": "ok"})
            except Exception as e:
                self._send_json({"error": str(e)}, 500)

    def build_tree(self, dir_path):
        tree = []
        try:
            for item in sorted(os.listdir(dir_path)):
                full_path = os.path.join(dir_path, item)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace('\\', '/')
                if os.path.isdir(full_path):
                    tree.append({
                        "name": item,
                        "type": "folder",
                        "path": rel_path,
                        "children": self.build_tree(full_path)
                    })
                else:
                    tree.append({
                        "name": item,
                        "type": "file",
                        "path": rel_path
                    })
        except Exception:
            pass
        return tree

def start_server():
    global httpd, is_running
    try:
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR, exist_ok=True)
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", PORT), CORSRequestHandler)
        is_running = True
        httpd.serve_forever()
    except Exception as e:
        is_running = False
        print("Server error:", e)

def toggle_server():
    global server_thread, httpd, is_running
    if not is_running:
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        btn_run.config(text="Stop Server", bg="#4CAF50", fg="white")
        lbl_status.config(text=f"Running on http://localhost:{PORT}\nFolder: {BASE_DIR}")
    else:
        if httpd:
            httpd.shutdown()
            httpd.server_close()
        is_running = False
        btn_run.config(text="Run Server", bg="#2196F3", fg="white")
        lbl_status.config(text="Stopped")

def choose_folder():
    global BASE_DIR
    folder = filedialog.askdirectory(initialdir=BASE_DIR, title="Select Storage Folder")
    if folder:
        BASE_DIR = os.path.abspath(folder)
        if is_running:
            lbl_status.config(text=f"Running on http://localhost:{PORT}\nFolder: {BASE_DIR}")
        else:
            lbl_status.config(text=f"Folder set to:\n{BASE_DIR}")

root = tk.Tk()
root.title("Vector Canvas Server")
root.geometry("350x200")
root.configure(padx=20, pady=20)

tk.Label(root, text="Server Control Panel", font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))
btn_folder = tk.Button(root, text="Select Storage Folder", command=choose_folder, width=25)
btn_folder.pack(pady=5)
btn_run = tk.Button(root, text="Run Server", command=toggle_server, bg="#2196F3", fg="white", font=("Segoe UI", 12, "bold"), width=20, height=2)
btn_run.pack(pady=10)
lbl_status = tk.Label(root, text="Stopped", fg="#555")
lbl_status.pack()

root.mainloop()
