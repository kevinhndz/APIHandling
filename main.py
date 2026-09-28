import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.handlers import ExcepcionesGlobales as EH

from modules.productos.router import router as router_productos
from modules.Clients.router import router as router_clients
from modules.usuarios.router import router as router_usuarios

# Configurar registros basicos en consola
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API")

app = FastAPI(
    title="Sistema de Almacen",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",  # Frontend comun (React/NextJS)
    "http://localhost:5173",  # Frontend comun (Vite/Vue/React)
    "*"                       # En desarrollo, '*' permite cualquier origen
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],      # Permite GET, POST, PUT, DELETE, PATCH, etc.
    allow_headers=["*"],      # Permite todos los headers (incluyendo el token de autorizacion)
)


# --- 2. Middleware Personalizado: Tiempo de Ejecución y Logs ---
@app.middleware("http")
async def medir_tiempo_respuesta(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request) 
    tiempo_proceso = (time.perf_counter() - inicio) * 1000  
    response.headers["X-Process-Time-Ms"] = f"{tiempo_proceso:.2f}"
    logger.info(f"Peticion: {request.method} {request.url.path} | Estado: {response.status_code} | Tiempo: {tiempo_proceso:.2f}ms")
    return response

# --- 3. Registrar Manejadores Globale de Excepciones ---
EH.registrar_handlers(app)


# --- 4. Registrar Rutas de los Módulos ---
app.include_router(router_productos)
app.include_router(router_clients)
app.include_router(router_usuarios)