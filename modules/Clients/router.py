from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from database.almacen import abrir_puerta
from modules.Clients.schema import (
    Revisar_JSON_Crear_Nuevo_Cliente, 
    Revisar_JSON_Editar_Cliente,
    Revisar_JSON_Editar_Cliente_Parcial
)
from modules.Clients.service import ClientsService as service
from utils.auth import permiso_admin, permiso_usuario

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    dependencies=[Depends(permiso_admin)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_nuevo_cliente(
    json: Revisar_JSON_Crear_Nuevo_Cliente, 
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.crear_cliente(db, json)

@router.get("/")
def obtener_clientes(
    salto: int = Query(default=0, ge=0),
    limite: int = Query(default=10, ge=1),
    db: Session = Depends(abrir_puerta),
    usuario: dict = Depends(permiso_admin)
):
    return service.obtener_clientes(db, salto, limite)

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