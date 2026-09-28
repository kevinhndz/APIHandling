from sqlalchemy.orm import Session
import logging  
from modules.Clients.repository import ClientsRepository as repo
from modules.Clients.model import Clients
from modules.usuarios.model import Users
from modules.Clients.schema import (
    Revisar_JSON_Crear_Nuevo_Cliente, 
    Revisar_JSON_Editar_Cliente,
    Revisar_JSON_Editar_Cliente_Parcial
)
from utils.hash import encriptar_contrasena
from core.exceptions import RecursoNoEncontradoError, RecursoDuplicadoError

logger = logging.getLogger("ClientesService")  

class ClientsService():
    
    @staticmethod
    def crear_cliente(db: Session, json: Revisar_JSON_Crear_Nuevo_Cliente):
        check = repo.revisar_duplicados(db, json)
        
        if check is not None:
            logger.warning(f"Intento crear cliente con email duplicado: {json.email}")  
            raise RecursoDuplicadoError("Cliente ya esta registrado")
        else:
            new_user = Users(
                user=json.user,
                password=encriptar_contrasena(json.password),
                rol=json.rol
            )
            
            new_u = repo.crear_nuevo_user(db, new_user)
            logger.info(f"Usuario creado para cliente: user={new_u.user}")  
                
            new_customer = Clients(
                nombre=json.nombre,
                email=json.email,
                id_user=new_user.id
            )
            
            new_c = repo.crear_nuevo_customer(db, new_customer)
            logger.info(f"Cliente creado: ID={new_c.id}, Email={new_c.email}")  
            return new_c

    @staticmethod
    def obtener_clientes(db: Session, salto: int, limite: int):
        result = repo.obtener_clientes_paginados(db, salto, limite)
        logger.info(f"Obtenidos {len(result)} clientes")  
        return result
    
    @staticmethod
    def editar_cliente(db: Session, json: Revisar_JSON_Editar_Cliente, id: int):
        check = repo.revisar_duplicados_por_ID_put(db, id)
        
        if check is not None:
            check.nombre = json.nombre
            check.email = json.email
            editado = repo.guardar_cambios_put(db, check)
            logger.info(f"Cliente actualizado: ID={id}")  
            return editado
        else:
            logger.warning(f"Intento actualizar cliente inexistente: ID={id}")  
            raise RecursoNoEncontradoError("No se encontro el recurso")

    @staticmethod
    def editar_cliente_parcial(db: Session, json: Revisar_JSON_Editar_Cliente_Parcial, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            logger.warning(f"Intento actualizar parcialmente cliente inexistente: ID={id}") 
            raise RecursoNoEncontradoError("No se encontro el recurso")
        
        datos_actualizar = json.model_dump(exclude_unset=True)
        
        for campo, valor in datos_actualizar.items():
            setattr(check, campo, valor)
            
        result = repo.guardar_cambios_patch(db, check)
        logger.info(f"Cliente actualizado parcialmente: ID={id}") 
        return result

    @staticmethod
    def eliminar_cliente(db: Session, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            logger.warning(f"Intento eliminar cliente inexistente: ID={id}") 
            raise RecursoNoEncontradoError("No se encontro el recurso")
            
        repo.eliminar_cliente(db, check)
        logger.info(f"Cliente eliminado: ID={id}")  
        return None