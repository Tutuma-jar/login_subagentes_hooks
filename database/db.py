"""Persistent SQLite users with PBKDF2 password hashes."""

from contextlib import closing
import hashlib
import hmac
from pathlib import Path
import secrets
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PBKDF2_ITERATIONS = 600_000
SALT_BYTES = 16
HASH_BYTES = 32


def _resolve_db_path(db_path):
    path = Path(db_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def init_db(db_path):
    """Create the schema and demo user without changing existing users."""
    path = _resolve_db_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.executescript(schema)
            existing = connection.execute(
                "SELECT id FROM users WHERE email = ?", ("demo@example.com",)
            ).fetchone()
            if existing is None:
                salt = secrets.token_bytes(SALT_BYTES)
                password_hash = hashlib.pbkdf2_hmac(
                    "sha256", b"Demo1234!", salt, PBKDF2_ITERATIONS
                ).hex()
                connection.execute(
                    "INSERT OR IGNORE INTO users "
                    "(name, email, password_hash, salt) VALUES (?, ?, ?, ?)",
                    ("Usuario Demo", "demo@example.com", password_hash, salt.hex()),
                )


def find_user_by_email(db_path, email):
    """Return all stored user fields, or None when the email is absent."""
    with closing(sqlite3.connect(_resolve_db_path(db_path))) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT id, name, email, password_hash, salt FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        return dict(row) if row is not None else None


def verify_password(password, password_hash, salt):
    """Verify a password; malformed password hashes or salts return False."""
    if not all(isinstance(value, str) for value in (password, password_hash, salt)):
        return False
    if len(password_hash) != HASH_BYTES * 2 or len(salt) != SALT_BYTES * 2:
        return False
    try:
        expected_hash = bytes.fromhex(password_hash)
        salt_bytes = bytes.fromhex(salt)
        if len(expected_hash) != HASH_BYTES or len(salt_bytes) != SALT_BYTES:
            return False
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt_bytes, PBKDF2_ITERATIONS
        )
    except (ValueError, UnicodeError):
        return False
    return hmac.compare_digest(actual_hash, expected_hash)
