import atexit
import json
import threading
import traceback
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

_DATA_FILE = Path(__file__).parent.parent / "data" / "bai50_state.json"
_LOG_FILE  = Path(__file__).parent.parent / "data" / "bai50_api.log"
_lock = threading.Lock()
_started = False

_DEFAULT_STATE = {"payer_profiles": []}


def _log(msg: str):
    """Append a timestamped log line (silent on failure)."""
    try:
        import datetime
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _LOG_FILE.parent.mkdir(exist_ok=True)
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass


# ── PDF via subprocess (avoids Playwright sync-API / asyncio thread conflicts) ─

def _render_pdf(html: str) -> bytes:
    """Render full HTML → PDF bytes via Playwright CLI subprocess."""
    import subprocess, sys, tempfile, os

    # Write HTML to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".html", delete=False
    ) as f:
        f.write(html)
        html_path = f.name

    pdf_path = html_path.replace(".html", ".pdf")
    try:
        script = f"""
import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(args=[
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-first-run',
        '--no-zygote',
    ])
    page = browser.new_page()
    page.set_content(open({repr(html_path)}, encoding='utf-8').read(),
                     wait_until='domcontentloaded', timeout=30000)
    page.pdf(path={repr(pdf_path)},
             format='A4',
             margin={{'top':'8mm','right':'10mm','bottom':'8mm','left':'10mm'}},
             print_background=True)
    browser.close()
"""
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode != 0:
            err = (result.stderr or result.stdout or "unknown").strip()
            _log(f"PDF subprocess error: {err}")
            raise RuntimeError(f"pdf_render_error: {err[:300]}")

        if not Path(pdf_path).exists():
            raise RuntimeError("pdf_render_error: output file not created")

        data = Path(pdf_path).read_bytes()
        if not data.startswith(b"%PDF"):
            raise RuntimeError("pdf_render_error: output is not a valid PDF")
        _log(f"PDF OK: {len(data)} bytes")
        return data

    finally:
        for p in (html_path, pdf_path):
            try:
                os.unlink(p)
            except Exception:
                pass


# ── JSON helpers ─────────────────────────────────────────────────────────────

def _read():
    if _DATA_FILE.exists():
        try:
            return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return dict(_DEFAULT_STATE)


def _write(data):
    _DATA_FILE.parent.mkdir(exist_ok=True)
    _DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── HTTP Handler ──────────────────────────────────────────────────────────────

class _Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path != "/bai50/profiles":
            self.send_response(404); self.end_headers(); return
        with _lock:
            body = json.dumps(_read(), ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw    = self.rfile.read(length)

        # ── profiles ──────────────────────────────────────────────────────────
        if self.path == "/bai50/profiles":
            data = json.loads(raw)
            with _lock:
                _write(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
            return

        # ── PDF generation ────────────────────────────────────────────────────
        if self.path == "/bai50/pdf":
            try:
                html = json.loads(raw).get("html", "")
                pdf_bytes = _render_pdf(html)
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(len(pdf_bytes)))
                self._cors()
                self.end_headers()
                self.wfile.write(pdf_bytes)
            except RuntimeError as e:
                _log(f"RuntimeError in /bai50/pdf: {e}")
                self._json_error(503, str(e))
            except Exception as e:
                _log(f"Exception in /bai50/pdf: {traceback.format_exc()}")
                self._json_error(500, str(e))
            return

        self.send_response(404)
        self.end_headers()

    def _json_error(self, code: int, msg: str):
        body = json.dumps({"error": msg}, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


# ── Start server ──────────────────────────────────────────────────────────────

def start(port=8504):
    global _started
    if _started:
        return
    _started = True
    _log(f"bai50_api starting on port {port}")
    server = ThreadingHTTPServer(("0.0.0.0", port), _Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
