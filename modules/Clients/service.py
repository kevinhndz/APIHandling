from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from modules.Clients.repository import ClientsRepository as repo
from modules.Clients.model import Clients
from modules.usuarios.model import Users
from modules.Clients.schema import (
    Revisar_JSON_Crear_Nuevo_Cliente, 
    Revisar_JSON_Editar_Cliente,
    Revisar_JSON_Editar_Cliente_Parcial
)
from utils.hash import encriptar_contrasena


class ClientsService():
    
    @staticmethod
    def crear_cliente(db: Session, json: Revisar_JSON_Crear_Nuevo_Cliente):
        check = repo.revisar_duplicados(db, json)
        
        if check is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cliente ya esta registrado"
            )
        else:
            new_user = Users(
                user=json.user,
                password=encriptar_contrasena(json.password),
                rol=json.rol
            )
            
            new_u = repo.crear_nuevo_user(db, new_user)
                
            new_customer = Clients(
                nombre=json.nombre,
                email=json.email,
                id_user=new_user.id
            )
            
            new_c = repo.crear_nuevo_customer(db, new_customer)
            return new_c

    @staticmethod
    def obtener_clientes(db: Session, salto: int, limite: int):
        return repo.obtener_clientes_paginados(db, salto, limite)
    
    @staticmethod
    def editar_cliente(db: Session, json: Revisar_JSON_Editar_Cliente, id: int):
        check = repo.revisar_duplicados_por_ID_put(db, id)
        
        if check is not None:
            check.nombre = json.nombre
            check.email = json.email
            editado = repo.guardar_cambios_put(db, check)
            return editado
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro el recurso"
            )

    @staticmethod
    def editar_cliente_parcial(db: Session, json: Revisar_JSON_Editar_Cliente_Parcial, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro el recurso"
            )
        
        datos_actualizar = json.model_dump(exclude_unset=True)
        
        for campo, valor in datos_actualizar.items():
            setattr(check, campo, valor)
            
        return repo.guardar_cambios_patch(db, check)

    @staticmethod
    def eliminar_cliente(db: Session, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro el recurso"
            )
            
        repo.eliminar_cliente(db, check)
        return None