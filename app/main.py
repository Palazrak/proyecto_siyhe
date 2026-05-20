from pathlib import Path
import hashlib

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Usuario
from .schemas import LoginPayload, PlacaPayload

app = FastAPI(title="Multas CDMX", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def unhandled_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/placas", response_class=HTMLResponse)
def placas_page(request: Request):
    return templates.TemplateResponse("placas.html", {"request": request})


@app.post("/api/login")
def login_or_create(payload: LoginPayload, db: Session = Depends(get_db)) -> JSONResponse:
    usuario = payload.usuario.strip()
    password = payload.password

    if not usuario or not password:
        raise HTTPException(status_code=400, detail="Usuario y contraseña son obligatorios")

    record = db.query(Usuario).filter(Usuario.usuario == usuario).first()

    if record:
        return JSONResponse({"status": "existing", "usuario": record.usuario, "id_usuario": record.id_usuario})

    hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    nuevo = Usuario(usuario=usuario, password_hash=hashed_password)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return JSONResponse({"status": "created", "usuario": nuevo.usuario, "id_usuario": nuevo.id_usuario})


@app.post("/api/placa")
def save_placa(payload: PlacaPayload, db: Session = Depends(get_db)) -> JSONResponse:
    usuario = payload.usuario.strip()
    placa = payload.placa.strip().upper()

    if not usuario or not placa:
        raise HTTPException(status_code=400, detail="Usuario y placa son obligatorios")

    record = db.query(Usuario).filter(Usuario.usuario == usuario).first()
    if not record:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    record.placa = placa
    db.commit()

    return JSONResponse({"status": "ok", "message": "Placa guardada correctamente", "placa": placa})
