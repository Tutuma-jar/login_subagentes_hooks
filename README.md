# Demo de inicio de sesión

Aplicación local con Python 3, SQLite y HTML/CSS/JavaScript, sin dependencias externas.

## Arranque

En PowerShell:

```powershell
git clone https://github.com/Tutuma-jar/login_subagentes_hooks.git
cd login_subagentes_hooks
python backend/server.py
```

Abre http://127.0.0.1:8000/ en el navegador. Detén el servidor con Ctrl+C.
El servidor crea automáticamente `database/login.sqlite3` y el usuario demo.

## Credenciales demo

- Correo: `demo@example.com`
- Contraseña: `Demo1234!`
- Nombre: Usuario Demo

Incluye inicio de sesión, bienvenida y cierre de sesión. Las sesiones se guardan
en memoria y se pierden al reiniciar el servidor. Los usuarios persisten en SQLite;
la contraseña se almacena como un hash PBKDF2 con sal aleatoria.

## Estructura

- `backend/server.py`: servidor local, API y archivos estáticos.
- `frontend/index.html`, `styles.css`, `app.js`: interfaz del navegador.
- `database/__init__.py`, `db.py`, `schema.sql`: acceso a SQLite y esquema.

La API usa `POST /api/login`, `GET /api/me` y `POST /api/logout` desde el mismo
origen. La sesión viaja en una cookie HttpOnly con SameSite=Strict.

## Pruebas

Desde la carpeta del proyecto:

```powershell
python -m unittest discover -s tests -v
```

La suite contiene cinco pruebas del login y la sesión. Las dos expectativas
intencionalmente incorrectas se corrigieron: una contraseña incorrecta y una
consulta a `/api/me` sin sesión deben devolver `401`. El resultado esperado
es cinco pruebas aprobadas (`OK`).

Las pruebas usan una base de datos temporal y un puerto local disponible;
no modifican `database/login.sqlite3`.

## GitHub Actions

El workflow `.github/workflows/login-tests.yml` ejecuta las cinco pruebas en
Python 3.14 al subir cambios a `main` o abrir un pull request hacia esa rama.
También puedes iniciarlo manualmente desde **Actions → Tests del login → Run workflow**.

Consulta las ejecuciones en
[Actions del repositorio](https://github.com/Tutuma-jar/login_subagentes_hooks/actions).
En el paso de unittest se muestran los resultados de las cinco pruebas.

## Hook de Git

Activa el hook local en cada clon del repositorio:

```powershell
git config --local core.hooksPath .githooks
```

Antes de cada commit, el hook `pre-commit` comprueba que los archivos del
proyecto estén agregados y ejecuta los tests. Si reaparecen los dos bloques
originales de fallo intencional, corrige sus expectativas de `200` a `401`,
renombra los tests y detiene el commit para revisar la corrección:

```powershell
git diff
git add tests/test_login.py
git commit -m "Corrige las expectativas del login"
```

Otros fallos bloquean el commit y requieren una corrección manual. El hook
no modifica el backend ni agrega archivos automáticamente. Puedes ejecutar
la corrección y los tests sin hacer un commit:

```powershell
python scripts/fix_login_tests.py
```
