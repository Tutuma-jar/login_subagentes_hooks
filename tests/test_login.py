"""Cinco pruebas HTTP del login y de la sesión."""

import http.client
from http.cookies import SimpleCookie
from http.server import HTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backend import server


class QuietLoginHandler(server.LoginHandler):
    def log_message(self, format, *args):
        pass


class LoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temp.cleanup)
        db_path = Path(temp.name) / "login.sqlite3"
        server.init_db(db_path)
        db_patch = patch.object(server, "DB_PATH", db_path)
        db_patch.start()
        cls.addClassCleanup(db_patch.stop)
        session_patch = patch.object(server, "SESSIONS", {})
        session_patch.start()
        cls.addClassCleanup(session_patch.stop)
        cls.httpd = HTTPServer(("127.0.0.1", 0), QuietLoginHandler)
        cls.addClassCleanup(cls.httpd.server_close)
        cls.thread = threading.Thread(
            target=cls.httpd.serve_forever,
            kwargs={"poll_interval": 0.01},
            daemon=True,
        )
        cls.thread.start()
        cls.addClassCleanup(cls.stop_server)

    @classmethod
    def stop_server(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=5)
        server.SESSIONS.clear()

    def setUp(self):
        server.SESSIONS.clear()

    def tearDown(self):
        server.SESSIONS.clear()

    def request(self, method, path, data=None, cookie=None):
        body = json.dumps(data).encode("utf-8") if data is not None else None
        headers = {"Content-Type": "application/json"}
        if cookie:
            headers["Cookie"] = cookie
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.httpd.server_port, timeout=5
        )
        try:
            connection.request(method, path, body=body, headers=headers)
            response = connection.getresponse()
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, dict(response.getheaders()), payload
        finally:
            connection.close()

    def login(self, password="Demo1234!"):
        return self.request(
            "POST", "/api/login",
            {"email": "demo@example.com", "password": password},
        )

    @staticmethod
    def session_cookie(headers):
        parsed = SimpleCookie()
        parsed.load(headers["Set-Cookie"])
        return f"session={parsed['session'].value}"

    def test_login_valido_cookie_y_usuario_publico(self):
        """Credenciales válidas crean una sesión sin exponer secretos."""
        status, headers, payload = self.login()
        self.assertEqual(status, 200)
        self.assertEqual(set(payload["user"]), {"id", "name", "email"})
        self.assertEqual(payload["user"]["email"], "demo@example.com")
        parsed = SimpleCookie()
        parsed.load(headers["Set-Cookie"])
        self.assertTrue(parsed["session"].value)
        self.assertTrue(parsed["session"]["httponly"])
        self.assertEqual(parsed["session"]["samesite"], "Strict")
        self.assertEqual(parsed["session"]["path"], "/")

    def test_rechaza_password_incorrecta(self):
        """Una contraseña incorrecta devuelve 401 y no crea una sesión."""
        status, headers, payload = self.login(password="incorrecta")
        self.assertEqual(status, 401)
        self.assertEqual(payload, {"error": "Credenciales inválidas"})
        self.assertNotIn("Set-Cookie", headers)
        self.assertFalse(server.SESSIONS)

    def test_sesion_persistente_y_logout(self):
        """La cookie autentica /api/me; logout invalida la sesión."""
        status, headers, login_payload = self.login()
        self.assertEqual(status, 200)
        cookie = self.session_cookie(headers)
        status, _, payload = self.request("GET", "/api/me", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertEqual(payload, login_payload)
        status, headers, payload = self.request(
            "POST", "/api/logout", cookie=cookie
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"ok": True})
        self.assertIn("Max-Age=0", headers["Set-Cookie"])
        status, _, _ = self.request("GET", "/api/me", cookie=cookie)
        self.assertEqual(status, 401)
        self.assertFalse(server.SESSIONS)

    def test_password_incorrecta_devuelve_401(self):
        """Una contraseña incorrecta debe devolver 401."""
        status, _, _ = self.login(password="incorrecta")
        self.assertEqual(status, 401)

    def test_me_sin_cookie_devuelve_401(self):
        """Consultar /api/me sin sesión debe devolver 401."""
        status, _, _ = self.request("GET", "/api/me")
        self.assertEqual(status, 401)


if __name__ == "__main__":
    unittest.main()
