from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database.almacen import abrir_puerta
from modules.productos.schema import (
    Revisar_JSON_Crear_Producto, 
    Revisar_JSON_Editar_Producto,
    Revisar_JSON_Editar_Producto_Parcial,
    ProductoRespuesta
)
from core.schema import RespuestaPaginada
from modules.productos.service import ProductosService as service
from utils.auth import permiso_admin, permiso_usuario

router = APIRouter(
    prefix="/products",
    tags=["Productos"],
    dependencies=[Depends(permiso_usuario)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_nuevo_producto(
    json: Revisar_JSON_Crear_Producto, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_usuario)
):
    return service.crear_producto(db, json)

@router.get("/",response_model=RespuestaPaginada[ProductoRespuesta],
    status_code=status.HTTP_200_OK)
def obtener_productos(
    salto: int = Query(default=0, ge=0),
    limite: int = Query(default=10, ge=1),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.obtener_productos_service(db, salto, limite)

@router.put("/{id}")
def editar(
    id: int, 
    json: Revisar_JSON_Editar_Producto, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.editar_producto(db, json, id)

@router.patch("/{id}")
def editar_parcial(
    id: int, 
    json: Revisar_JSON_Editar_Producto_Parcial, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.editar_producto_parcial(db, json, id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    id: int, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.eliminar_producto(db, id)