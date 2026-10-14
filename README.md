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

La suite contiene cinco pruebas: tres deben pasar y dos fallan intencionalmente
con expectativas incorrectas para demostrar un resultado fallido. Sus nombres
empiezan con `test_fallo_intencional_`. El resultado esperado es
`FAILED (failures=2)` y el comando termina con código de salida 1.

Las pruebas usan una base de datos temporal y un puerto local disponible;
no modifican `database/login.sqlite3`.
