import os
import sys
import time
import json
import http.server
import socketserver
import threading
import urllib.parse
import shutil
import base64

if sys.platform == 'win32':
    os.system('')

BLUE = "\033[94m"
RESET = "\033[0m"

BANNER = BLUE + r"""                                                                    
                                                                                             
                  ▓███▓░                                                                     
                  ▓█▓░▓█████░                                                                
                  ▒▓█▓▓   █████▓                 ▓                                           
                   ▓██▓▓▓   ░█████▓             ░                                            
                    ▒▓██▓▓▒   ███████▒                                                       
                      ▓██▓▓▓   ▓███████▒                                                     
                       ▓██▓▓     ▓███████░                   ░                               
                       ▒▓██▓▓░     ███████▒                                                  
                        ▓▓██▓▓▒      ██████   ▒▒░   ░                                        
                         ▓▓██▓▓       █████▓▓▒▓▓▓░                                           
                          ▓▓██▓▓▓      ████▓█▓▓▒▒░                                           
                           ▓▓█▓▓▓      ▓██▓▓▓▓▓████████████▓                                 
                           █▓▓▓▓▓░     █▓▓█▓▓███████████████████▒                            
                          ░█▓▓▓▓▓▓    ▒▓▓▓▓▓██▓░▒░░░▓▓██████████████                         
                          ██░█▓▓▓▓   ▓▓▓▓▓░                ░▓█████████▓                      
                          ▓▒ █▓▓▓▓ ░▓▓▓▓                         ░  ▒▓▓▓▓░                   
                          ██ █▓▓▓▒ ▓▓▓   ▓▓▓▓▓▓███████████████████▓▓▓░ ░▓▒▓                  
                          ░▓▒█▓▓▓░▓░ ░▓▓▓▓▓▓▓▓▓▓▓██████████████████████▓▓▓██░                
                         ░██░▓▓▓▒▓▓▓▓▓▓▓▓█▓  ▓██                 ░▒▓▓▓▓▓▒░                   
                          ░█▓▓▓▓▓▓▓▓██░█▒▓███░                                               
                          ▒▓▓▓▓▓█████▒ ░▒                                                    
                         ▓▓▓▓▓▓░  ░                                                          
                           ░▓                                                                
                                                                                                                                                                                
        GRAPHIUM  SARPEDON    1.0.0
""" + RESET

HELP_TEXT = """This is the local storage server for Graphium Sarpedon.

  /start    start the server
  /stop     stop the server
  /status   show whether the server is running, and where notes are stored
  /exit     stop the server (if running) and quit
  /help     show this message
"""

server_thread = None
httpd = None
is_running = False
PORT = 8080


def get_base_dir():
    """
    Resolve the storage folder as "<the folder this app lives in>/memory".

    When this script is frozen into a standalone executable (e.g. with
    PyInstaller), __file__ points at a temporary extraction directory rather
    than the real location of the .exe on disk. That mismatch is what used
    to make the app silently create a brand-new, empty "memory" folder
    somewhere else instead of using the one already sitting right next to
    it. sys.frozen / sys.executable resolve correctly in that case, so this
    always finds the real, existing folder next to the actual program.
    """
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, "memory")


BASE_DIR = get_base_dir()


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

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


def _serve():
    global httpd, is_running
    try:
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(("", PORT), CORSRequestHandler)
        is_running = True
        httpd.serve_forever()
    except Exception as e:
        is_running = False
        print(f"\n[error] Could not start server: {e}")


def stop_server_internal():
    global httpd, is_running
    if httpd:
        httpd.shutdown()
        httpd.server_close()
    is_running = False

def cmd_start():
    global server_thread, is_running

    if is_running:
        print("Server is already running.")
        return

    existed = os.path.isdir(BASE_DIR)
    os.makedirs(BASE_DIR, exist_ok=True)
    if existed:
        try:
            count = len(os.listdir(BASE_DIR))
        except Exception:
            count = "?"
        print(f"Using existing storage folder ({count} item(s) found).")
    else:
        print("Storage folder did not exist yet - created a new, empty one.")
    print(f"Folder: {BASE_DIR}")

    server_thread = threading.Thread(target=_serve, daemon=True)
    server_thread.start()
    time.sleep(0.25)

    if is_running:
        print(f"Server running at http://localhost:{PORT}")
    else:
        print("Server failed to start (see error above).")


def cmd_stop():
    if not is_running:
        print("Server is not running.")
        return
    stop_server_internal()
    print("Server stopped.")


def cmd_status():
    if is_running:
        print(f"Status: running at http://localhost:{PORT}")
    else:
        print("Status: stopped")
    print(f"Storage folder: {BASE_DIR}")


def main():
    print(BANNER)
    print(HELP_TEXT)

    while True:
        try:
            raw = input("graphium> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw:
            continue

        cmd = raw.lower()
        if cmd == '/help':
            print(HELP_TEXT)
        elif cmd == '/start':
            cmd_start()
        elif cmd == '/stop':
            cmd_stop()
        elif cmd == '/status':
            cmd_status()
        elif cmd in ('/exit', '/quit'):
            break
        else:
            print(f"Unknown command: {raw}. Type /help for a list of commands.")

    if is_running:
        stop_server_internal()
    print("Goodbye.")


if __name__ == '__main__':
    main()
