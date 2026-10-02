import logging
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.handlers import ExcepcionesGlobales
from modules.Clients.router import router as router_clientes
from modules.productos.router import router as router_productos
from modules.usuarios.router import router as router_usuarios


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

app = FastAPI(title="Sistema de Almacen", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ExcepcionesGlobales.registrar_handlers(app)
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
    logger.info(
        "%s %s | %s | %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        tiempo,
    )
    return response


# Keep the static frontend last so API routes take precedence.
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
