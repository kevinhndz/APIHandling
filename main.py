import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
from core.handlers import ExcepcionesGlobales as EH

from modules.productos.router import router as router_productos
from modules.Clients.router import router as router_clientes
from modules.usuarios.router import router as router_usuarios

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

app = FastAPI(title="Sistema de Almacen", version="1.0.0")

# CORS - Permite todo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de API
EH.registrar_handlers(app)
app.include_router(router_productos)
app.include_router(router_clientes)
app.include_router(router_usuarios)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.middleware("http")
async def medir_tiempo(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    tiempo = (time.perf_counter() - inicio) * 1000
    response.headers["X-Process-Time-Ms"] = f"{tiempo:.2f}"
    logger.info(f"{request.method} {request.url.path} | {response.status_code} | {tiempo:.2f}ms")
    return response

