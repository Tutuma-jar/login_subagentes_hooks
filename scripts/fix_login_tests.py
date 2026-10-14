"""Corrige los dos fallos conocidos y ejecuta los tests; no adivina otras correcciones."""

from pathlib import Path
import subprocess
import sys
from textwrap import dedent


PROJECT_DIR = Path(__file__).resolve().parents[1]
TEST_FILE = PROJECT_DIR / "tests" / "test_login.py"
REPAIRS = (
    (
        "test_fallo_intencional_password_incorrecta_aceptada",
        dedent('''\
            def test_fallo_intencional_password_incorrecta_aceptada(self):
                """Fallo intencional: el contrato correcto devuelve 401, no 200."""
                status, _, _ = self.login(password="incorrecta")
                self.assertEqual(
                    status, 200,
                    "FALLO INTENCIONAL: contraseña incorrecta debe devolver 401.",
                )'''),
        dedent('''\
            def test_password_incorrecta_devuelve_401(self):
                """Una contraseña incorrecta debe devolver 401."""
                status, _, _ = self.login(password="incorrecta")
                self.assertEqual(status, 401)'''),
    ),
    (
        "test_fallo_intencional_me_sin_cookie_autorizado",
        dedent('''\
            def test_fallo_intencional_me_sin_cookie_autorizado(self):
                """Fallo intencional: sin cookie corresponde 401, no 200."""
                status, _, _ = self.request("GET", "/api/me")
                self.assertEqual(
                    status, 200,
                    "FALLO INTENCIONAL: /api/me sin sesión debe devolver 401.",
                )'''),
        dedent('''\
            def test_me_sin_cookie_devuelve_401(self):
                """Consultar /api/me sin sesión debe devolver 401."""
                status, _, _ = self.request("GET", "/api/me")
                self.assertEqual(status, 401)'''),
    ),
)


def repair_source(source):
    """Reemplaza únicamente los bloques originales reconocidos, sin cambiar otros tests."""
    repaired = source
    changes = []
    for name, original, replacement in REPAIRS:
        old_block = "\n".join("    " + line for line in original.splitlines())
        new_block = "\n".join("    " + line for line in replacement.splitlines())
        if f"def {name}(" not in repaired:
            continue
        if repaired.count(old_block) != 1:
            raise ValueError(f"{name} fue editado: necesita revisión manual.")
        repaired = repaired.replace(old_block, new_block, 1)
        changes.append(name)
    if changes and "test_fallo_intencional_" not in repaired:
        repaired = repaired.replace(
            '"""Cinco pruebas HTTP: tres correctas y dos fallos intencionales."""',
            '"""Cinco pruebas HTTP del login y de la sesión."""',
            1,
        )
    return repaired, changes


def main():
    pre_commit = "--pre-commit" in sys.argv[1:]
    if pre_commit:
        result = subprocess.run(["git", "diff", "--quiet"], cwd=PROJECT_DIR)
        if result.returncode:
            print("Hay cambios sin agregar. Revisa y agrega los archivos antes del commit.")
            return 1
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "--",
             "backend", "database", "frontend", "tests", "scripts", ".githooks"],
            cwd=PROJECT_DIR, capture_output=True, text=True, check=True,
        )
        if untracked.stdout.strip():
            print("Hay archivos del proyecto sin agregar. Agrégalos antes del commit.")
            return 1

    try:
        source = TEST_FILE.read_text(encoding="utf-8")
        repaired, changes = repair_source(source)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"No se pudo corregir automáticamente: {error}", file=sys.stderr)
        return 1
    if changes:
        TEST_FILE.write_text(repaired, encoding="utf-8")
        print(f"Corregidas {len(changes)} expectativas: 200 -> 401.", flush=True)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=PROJECT_DIR,
    )
    if result.returncode:
        print("Los tests fallaron. Corrige el problema antes del commit.")
        return result.returncode
    if changes and pre_commit:
        print("Tests corregidos. Revisa git diff, ejecuta git add tests/test_login.py y repite el commit.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
