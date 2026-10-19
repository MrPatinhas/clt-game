import sys
import os
import json
import uuid
import time
import threading
import mimetypes
from pathlib import Path
from http.cookies import SimpleCookie
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Tuple, Optional

sys.stdout.reconfigure(encoding="utf-8")

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
STATIC_DIR = APP_DIR / "static"
ASSETS_DIR = ROOT_DIR / "assets"

sys.path.insert(0, str(APP_DIR))
from engine.game_state import CLTDataStore, CLTGameEngine

# Shared, immutable read-only historical lookup tables (~30 MB in RAM)
STORE = CLTDataStore()


class SessionManager:
    """Thread-safe multi-tenant in-memory session manager.
    
    Each visiting user/browser gets an isolated CLTGameEngine instance
    while sharing the read-only CLTDataStore lookup singleton in memory.
    """

    def __init__(self, data_store: CLTDataStore, ttl_seconds: int = 7200):
        self.store = data_store
        self.ttl = ttl_seconds
        self.sessions: Dict[str, Tuple[CLTGameEngine, float]] = {}
        self.lock = threading.Lock()

        # Start background cleaner thread (runs every 10 minutes)
        self.cleaner = threading.Thread(target=self._cleaner_loop, daemon=True)
        self.cleaner.start()

    def get_or_create(self, session_id: Optional[str]) -> Tuple[str, CLTGameEngine, bool]:
        with self.lock:
            now = time.time()
            if session_id and session_id in self.sessions:
                engine, _ = self.sessions[session_id]
                self.sessions[session_id] = (engine, now)
                return session_id, engine, False

            # New session
            new_id = uuid.uuid4().hex
            new_engine = CLTGameEngine(self.store)
            self.sessions[new_id] = (new_engine, now)
            return new_id, new_engine, True

    def reset_session(self, session_id: str) -> CLTGameEngine:
        with self.lock:
            new_engine = CLTGameEngine(self.store)
            self.sessions[session_id] = (new_engine, time.time())
            return new_engine

    def _cleaner_loop(self):
        while True:
            time.sleep(600)
            with self.lock:
                now = time.time()
                expired = [sid for sid, (_, last) in self.sessions.items() if now - last > self.ttl]
                for sid in expired:
                    del self.sessions[sid]
                if expired:
                    print(f"🧹 Cleaned {len(expired)} expired session(s). Active sessions: {len(self.sessions)}", flush=True)


SESSIONS = SessionManager(STORE)


class CLTRequestHandler(BaseHTTPRequestHandler):
    def _extract_session_id(self) -> Tuple[Optional[str], dict]:
        # 1. Cookie check
        cookie_header = self.headers.get("Cookie")
        session_id = None
        if cookie_header:
            cookie = SimpleCookie()
            try:
                cookie.load(cookie_header)
                if "clt_session_id" in cookie:
                    session_id = cookie["clt_session_id"].value
            except Exception:
                pass

        # 2. X-Session-ID header fallback
        if not session_id:
            session_id = self.headers.get("X-Session-ID")

        # 3. Query string fallback (?session_id=...)
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if not session_id and "session_id" in qs:
            session_id = qs["session_id"][0]

        return session_id, qs

    def _send_json(self, data: dict, status: int = 200, session_id: Optional[str] = None, is_new: bool = False):
        if session_id and isinstance(data, dict):
            data["session_id"] = session_id
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        if is_new and session_id:
            # Set cookie for 30 days
            self.send_header("Set-Cookie", f"clt_session_id={session_id}; Path=/; Max-Age=2592000; SameSite=Lax")
            self.send_header("X-Session-ID", session_id)
        self.end_headers()
        self.wfile.write(payload)

    def _serve_file(self, file_path: Path, session_id: Optional[str] = None, is_new: bool = False):
        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, "File not found")
            return
        mime, _ = mimetypes.guess_type(str(file_path))
        mime_str = mime or "application/octet-stream"
        if mime_str.startswith("text/") or mime_str == "application/javascript":
            mime_str += "; charset=utf-8"
        content = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime_str)
        self.send_header("Content-Length", str(len(content)))
        if is_new and session_id:
            self.send_header("Set-Cookie", f"clt_session_id={session_id}; Path=/; Max-Age=2592000; SameSite=Lax")
            self.send_header("X-Session-ID", session_id)
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)
        raw_sid, _ = self._extract_session_id()
        session_id, engine, is_new = SESSIONS.get_or_create(raw_sid)

        if parsed.path == "/api/state":
            self._send_json(engine.state, session_id=session_id, is_new=is_new)
        elif parsed.path == "/" or parsed.path == "/index.html":
            self._serve_file(STATIC_DIR / "index.html", session_id=session_id, is_new=is_new)
        elif parsed.path == "/health":
            self._send_json({"status": "ok", "active_sessions": len(SESSIONS.sessions)})
        elif parsed.path.startswith("/static/"):
            rel = parsed.path[len("/static/"):]
            self._serve_file(STATIC_DIR / rel)
        elif parsed.path.startswith("/assets/"):
            rel = parsed.path[len("/assets/"):]
            self._serve_file(ASSETS_DIR / rel)
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        raw_sid, _ = self._extract_session_id()
        session_id, engine, is_new = SESSIONS.get_or_create(raw_sid)

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        try:
            if parsed.path == "/api/new-run":
                # Start fresh run on this session's engine
                new_state = engine.start_new_run()
                self._send_json(new_state, session_id=session_id, is_new=is_new)

            elif parsed.path == "/api/select-rooster":
                self._send_json(
                    engine.select_rooster(
                        rooster_index=int(body.get("rooster_index", 0)),
                        ai_difficulty=body.get("ai_difficulty", "veteran"),
                        series_mode=body.get("series_mode", "bo3"),
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage2/swap-order":
                self._send_json(
                    engine.prepare_stage_2(first_chooser=body.get("first_chooser")),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage2/submit":
                self._send_json(
                    engine.submit_stage_2_parameter(
                        param_type=body.get("param_type", "round"),
                        value=int(body.get("value", 1)),
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage3/submit":
                self._send_json(
                    engine.submit_stage_3_bucket(
                        action=body.get("action", "pass"),
                        bucket_player_id=body.get("bucket_player_id"),
                        dropped_player_id=body.get("dropped_player_id"),
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage4/submit":
                self._send_json(
                    engine.submit_stage_4_highlights(
                        choice_mode=body.get("choice_mode", "5_matches")
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage5/reroll":
                self._send_json(
                    engine.prepare_stage_5(force_rule_id=body.get("rule_id")),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage5/proceed":
                self._send_json(
                    engine.prepare_stage_6(),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage6/submit":
                self._send_json(
                    engine.submit_stage_6_lineup(
                        formation=body.get("formation", "4-3-3"),
                        starter_ids=body.get("starter_ids", []),
                        captain_id=int(body.get("captain_id", 0)),
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage7/powerup":
                self._send_json(
                    engine.use_stage_7_powerup(
                        powerup_id=body.get("powerup_id", ""),
                        target_opponent_id=body.get("target_opponent_id"),
                        target_own_id=body.get("target_own_id"),
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage7/submit":
                self._send_json(
                    engine.submit_stage_7_halftime(
                        formation=body.get("formation", "4-3-3"),
                        final_starter_ids=body.get("final_starter_ids", []),
                        captain_id=int(body.get("captain_id", 0)),
                    ),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/stage8/next-match":
                self._send_json(
                    engine.advance_to_next_match(),
                    session_id=session_id,
                    is_new=is_new,
                )

            elif parsed.path == "/api/set-stage":
                target = int(body.get("stage", 1))
                engine.state["stage"] = target
                self._send_json(engine.state, session_id=session_id, is_new=is_new)

            else:
                self.send_error(404, "Unknown endpoint")
        except Exception as e:
            self._send_json({"error": str(e)}, status=400, session_id=session_id, is_new=is_new)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    server = ThreadingHTTPServer((host, port), CLTRequestHandler)
    print(f"⏳ CLT Server running on {host}:{port}", flush=True)
    server.serve_forever()
