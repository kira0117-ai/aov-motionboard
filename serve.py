#!/usr/bin/env python3
"""
影片 Demo 生成器 · 本機伺服器
用法: python serve.py
"""
import http.server, json, threading, webbrowser, urllib.parse
from pathlib import Path

PORT = 8765
BASE = Path(__file__).parent

_state = {'ready': False, 'url': None, '_abs': None}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        p = self.path.split('?')[0]
        if p == '/api/status':
            self._json({'ready': _state['ready'], 'url': _state['url']})
        elif p.startswith('/video/'):
            self._serve_video(urllib.parse.unquote(p[7:]))
        elif p in ('/', ''):
            self._serve_file(BASE / 'index.html', 'text/html; charset=utf-8')
        else:
            fpath = BASE / p.lstrip('/')
            if fpath.exists() and fpath.is_file():
                ct = 'text/html; charset=utf-8' if p.endswith('.html') else 'application/octet-stream'
                self._serve_file(fpath, ct)
            else:
                self.send_error(404)

    def do_POST(self):
        if self.path == '/api/video_ready':
            n = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(n))
            ap = body.get('path', '')
            if ap and Path(ap).exists():
                _state['_abs'] = ap
                _state['url'] = '/video/' + urllib.parse.quote(Path(ap).name)
                _state['ready'] = True
                self._json({'ok': True})
                print(f'\n✅ 影片就緒：{ap}')
                print('   → H5 頁面即將自動載入\n')
            else:
                self._json({'ok': False, 'error': 'file not found'})
        else:
            self.send_error(404)

    def _serve_video(self, fname):
        ap = _state.get('_abs')
        if ap and Path(ap).name == fname and Path(ap).exists():
            data = Path(ap).read_bytes()
            self.send_response(200)
            self._cors()
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404)

    def _serve_file(self, path, ct):
        if not Path(path).exists():
            self.send_error(404)
            return
        data = Path(path).read_bytes()
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', ct)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, d):
        data = json.dumps(d).encode()
        self.send_response(200)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, fmt, *args):
        if args and '/api/status' not in str(args[0]):
            print(f'  {args[0]}')


if __name__ == '__main__':
    idx = BASE / 'index.html'
    if not idx.exists():
        print('⚠️  找不到 index.html，請確認 H5 頁面已另存為 index.html 放在同一目錄')

    print(f'\n🚀 影片 Demo 生成器 · 本機伺服器')
    print(f'   網址：http://localhost:{PORT}')
    print(f'   目錄：{BASE}')
    print('   按 Ctrl+C 停止\n')

    threading.Timer(1.2, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
    srv = http.server.HTTPServer(('localhost', PORT), Handler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\n🛑 已停止')
