from fastapi import FastAPI
from database.almacen import miclaseBase, motor
from modules.productos.router import router as router_productos
from modules.Clients.router import router as router_clients
from modules.usuarios.router import router as router_usuarios

app = FastAPI(
    title="Sistema de Almacen",
    version="1.0.0"
)


# Registrar rutas del modulo de productos
app.include_router(router_productos)
app.include_router(router_clients)
app.include_router(router_usuarios)