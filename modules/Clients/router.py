from fastapi import FastAPI , APIRouter,Depends
from modules.Clients.schema import Revisar_JSON_Crear_Nuevo_Cliente, Revisar_JSON_Editar_Cliente
from modules.Clients.model import Clients
from database.almacen import abrir_puerta
from sqlalchemy.orm import Session
from modules.Clients.service import ClientsService as service
from utils.auth import permiso_admin

router = APIRouter(
    prefix = "/clients",
    tags = ["Clients"],
    dependencies= [Depends(permiso_admin)]
)

@router.post("/", status_code= 201)
def crear_nuevo_cliente(json:Revisar_JSON_Crear_Nuevo_Cliente, db: Session = Depends(abrir_puerta)):
    return service.crear_cliente(db,json)

@router.put("/{id}")
def editar(id: int, json: Revisar_JSON_Editar_Cliente, db: Session = Depends(abrir_puerta)):
    return service.editar_cliente(db,json, id)


