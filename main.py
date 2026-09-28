import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.handlers import GlobalExceptionHandler as EH

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


@app.middleware("http")
def medir_tiempo_respuesta(request: Request, call_next):
    # PASO 1: Arrancar el cronometro
    inicio = time.perf_counter()
    
    # PASO 2: Dejar pasar la peticion hacia los routers
    response = call_next(request)
    
    # PASO 3: Calcular cuantos milisegundos pasaron desde que entro hasta que salio
    tiempo_proceso = (time.perf_counter() - inicio) * 1000
    
    # PASO 4: Pegarle una etiqueta a la respuesta con el tiempo que tardo
    response.headers["X-Process-Time-Ms"] = f"{tiempo_proceso:.2f}"
    
    # PASO 5: Imprimir el reporte en la consola de tu terminal
    logger.info(f"Peticion: {request.method} {request.url.path} | Estado: {response.status_code} | Tiempo: {tiempo_proceso:.2f}ms")
    
    # PASO 6: Devolver la respuesta al cliente
    return response

# --- 3. Registrar Manejadores Globale de Excepciones ---
EH.registrar_handlers(app)


# --- 4. Registrar Rutas de los Módulos ---
app.include_router(router_productos)
app.include_router(router_clients)
app.include_router(router_usuarios)