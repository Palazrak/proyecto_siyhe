# Proyecto Multas CDMX (FastAPI + PostgreSQL + Render)

Este proyecto incluye:
- Login que registra usuario si no existe (contraseña hasheada).
- Vista para capturar placa.
- API FastAPI para guardar/consultar en PostgreSQL.
- Configuración lista para desplegar en Render.

## Estructura

- `app/main.py`: app FastAPI, rutas HTML y API.
- `app/models.py`: modelo `usuarios`.
- `app/templates/login.html`: vista login.
- `app/templates/placas.html`: vista placas.
- `app/static/js/login.js`: flujo de login.
- `app/static/js/placas.js`: flujo de guardado de placa.
- `render.yaml`: infraestructura para Render (web + postgres).

## Tabla PostgreSQL

Tabla `usuarios`:
- `id_usuario`: entero secuencial con secuencia iniciando en `0`.
- `usuario`: texto único.
- `password_hash`: texto.
- `placa`: texto (última placa guardada para ese usuario).

## Ejecutar local

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Crea tu archivo `.env`:

```bash
cp .env.example .env
```

3. Levanta PostgreSQL con Docker:

```bash
docker compose up -d
```

4. Inicia servidor:

```bash
uvicorn app.main:app --reload
```

5. Abre `http://localhost:8000`.

Notas:
- El backend carga automáticamente variables de entorno desde `.env`.
- Si no quieres Docker, puedes usar cualquier PostgreSQL y actualizar `DATABASE_URL` en `.env`.

## Despliegue en Render

1. Sube este proyecto a un repositorio GitHub.
2. En Render, usa `New +` -> `Blueprint` y selecciona el repo.
3. Render leerá `render.yaml` y creará:
- Servicio web `multas-cdmx-web`
- Base PostgreSQL `multas-cdmx-db`
4. Al terminar, prueba la URL pública de Render.

## Dominio personalizado `multas.cdmx.mx`

Para usar exactamente `multas.cdmx.mx`, necesitas control DNS del dominio `cdmx.mx`.

1. En Render, entra al servicio web -> `Settings` -> `Custom Domains`.
2. Agrega `multas.cdmx.mx`.
3. Render te mostrará el registro DNS (generalmente `CNAME`) que debes crear en el proveedor DNS del dominio.
4. Espera propagación DNS y luego valida HTTPS automático en Render.

## Flujo implementado

1. Usuario captura `usuario` y `contraseña` en login.
2. `POST /api/login`:
- Si usuario existe: no crea registro nuevo.
- Si no existe: crea registro con contraseña hasheada (`bcrypt`).
3. Se abre `/placas`.
4. Usuario captura placa y presiona `Buscar`.
5. Se abre un modal de aviso de phishing con enlace al formulario:
`https://forms.gle/q3qekq8hoABuFTcg9`
6. En este flujo de simulación no se envían ni guardan datos al presionar `Buscar`.
