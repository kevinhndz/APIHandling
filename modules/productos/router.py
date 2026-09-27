from fastapi import FastAPI, APIRouter, Depends, status
from modules.Clients.schema import (
    Revisar_JSON_Crear_Nuevo_Cliente, 
    Revisar_JSON_Editar_Cliente,
    Revisar_JSON_Editar_Cliente_Parcial
)
from modules.Clients.model import Clients
from database.almacen import abrir_puerta
from sqlalchemy.orm import Session
from modules.Clients.service import ClientsService as service
from utils.auth import permiso_admin, permiso_usuario


router = APIRouter(
    prefix="/products",
    tags=["Productos"],
    dependencies=[Depends(permiso_usuario)]  
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_nuevo_cliente(
    json: Revisar_JSON_Crear_Nuevo_Cliente, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_usuario)  
):
    return service.crear_cliente(db, json)

@router.put("/{id}")
def editar(
    id: int, 
    json: Revisar_JSON_Editar_Cliente, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)  
):
    return service.editar_cliente(db, json, id)

@router.patch("/{id}")
def editar_parcial(
    id: int, 
    json: Revisar_JSON_Editar_Cliente_Parcial, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)  
):
    return service.editar_cliente_parcial(db, json, id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    id: int, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)  
):
    return service.eliminar_cliente(db, id)