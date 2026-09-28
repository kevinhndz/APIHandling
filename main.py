from fastapi import FastAPI
from core.handlers import ExcepcionesGlobales as eG

from modules.productos.router import router as router_productos
from modules.Clients.router import router as router_clients
from modules.usuarios.router import router as router_usuarios

app = FastAPI(
    title="Sistema de Almacen",
    version="1.0.0"
)

# --- Registrar Manejadores de Excepciones ---
eG.registrar_handlers(app)
# --- Registrar Rutas de los Módulos ---
app.include_router(router_productos)
app.include_router(router_clients)
app.include_router(router_usuarios)