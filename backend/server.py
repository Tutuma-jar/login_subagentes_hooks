"""Servidor de la demo; las sesiones en memoria se pierden al reiniciarlo."""

import json
import mimetypes
from pathlib import Path
import secrets
import sqlite3
import sys
from http import HTTPStatus
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlsplit


PROJECT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = (PROJECT_DIR / "frontend").resolve()
DB_PATH = PROJECT_DIR / "database" / "login.sqlite3"
sys.path.insert(0, str(PROJECT_DIR))

from database import find_user_by_email, init_db, verify_password


SESSIONS = {}
MAX_BODY_BYTES = 64 * 1024


class LoginHandler(BaseHTTPRequestHandler):
    server_version = "LoginDemo"
    sys_version = ""

    def send_json(self, status, payload, cookie=None):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if cookie is not None:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_error(self, code, message=None, explain=None):
        self.send_json(code, {"error": HTTPStatus(code).phrase})

    def session_id(self):
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
        except CookieError:
            return None
        session = cookie.get("session")
        return session.value if session else None

    def request_path(self):
        try:
            return urlsplit(self.path).path
        except ValueError:
            self.send_json(400, {"error": "Ruta inválida"})
            return None

    def do_GET(self):
        path = self.request_path()
        if path is None:
            return
        if path == "/api/me":
            user = SESSIONS.get(self.session_id())
            if user is None:
                self.send_json(401, {"error": "Sesión no válida"})
            else:
                self.send_json(200, {"user": user})
            return
        if path.startswith("/api/"):
            self.send_json(404, {"error": "Ruta no encontrada"})
            return
        self.serve_frontend(path)

    def do_POST(self):
        path = self.request_path()
        if path is None:
            return
        if path == "/api/logout":
            SESSIONS.pop(self.session_id(), None)
            self.send_json(
                200,
                {"ok": True},
                "session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0; "
                "Expires=Thu, 01 Jan 1970 00:00:00 GMT",
            )
            return
        if path != "/api/login":
            self.send_json(404, {"error": "Ruta no encontrada"})
            return
        self.login()

    def login(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Longitud de contenido inválida"})
            return
        if self.headers.get("Transfer-Encoding") or length <= 0:
            self.send_json(400, {"error": "Se requiere un cuerpo JSON válido"})
            return
        if length > MAX_BODY_BYTES:
            self.send_json(413, {"error": "Solicitud demasiado grande"})
            return
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError):
            self.send_json(400, {"error": "JSON inválido"})
            return
        if not isinstance(data, dict) or not all(
            isinstance(data.get(field), str) for field in ("email", "password")
        ):
            self.send_json(400, {"error": "Email y contraseña son obligatorios y deben ser cadenas"})
            return
        if not data["email"] or not data["password"]:
            self.send_json(400, {"error": "Email y contraseña son obligatorios"})
            return
        try:
            user = find_user_by_email(DB_PATH, data["email"])
            authenticated = user is not None and verify_password(
                data["password"], user["password_hash"], user["salt"]
            )
        except (sqlite3.Error, OSError, ValueError):
            self.send_json(500, {"error": "No se pudo procesar el inicio de sesión"})
            return
        if not authenticated:
            self.send_json(401, {"error": "Credenciales inválidas"})
            return
        public_user = {field: user[field] for field in ("id", "name", "email")}
        SESSIONS.pop(self.session_id(), None)
        session_id = secrets.token_urlsafe(32)
        SESSIONS[session_id] = public_user
        self.send_json(
            200,
            {"user": public_user},
            f"session={session_id}; HttpOnly; SameSite=Strict; Path=/",
        )

    def serve_frontend(self, request_path):
        relative_path = unquote(request_path).lstrip("/") or "index.html"
        try:
            target = (FRONTEND_DIR / relative_path).resolve()
            if not target.is_relative_to(FRONTEND_DIR):
                self.send_json(403, {"error": "Acceso denegado"})
                return
            if not target.is_file():
                self.send_json(404, {"error": "Archivo no encontrado"})
                return
            body = target.read_bytes()
        except (OSError, ValueError, RuntimeError):
            self.send_json(404, {"error": "Archivo no disponible"})
            return
        content_type = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        if target.suffix.lower() in (".html", ".css", ".js"):
            content_type += "; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


def main():
    try:
        init_db(DB_PATH)
        server = HTTPServer(("127.0.0.1", 8000), LoginHandler)
    except (sqlite3.Error, OSError):
        print("No se pudo inicializar la demo o abrir el puerto 8000.", file=sys.stderr)
        return 1
    print("Demo disponible en http://127.0.0.1:8000/ (Ctrl+C para detener).")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        SESSIONS.clear()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
