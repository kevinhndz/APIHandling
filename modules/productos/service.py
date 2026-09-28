from sqlalchemy.orm import Session
import logging  #
from modules.productos.repository import ProductosRepository as repo
from modules.productos.model import Productos
from modules.productos.schema import (
    Revisar_JSON_Crear_Producto, 
    Revisar_JSON_Editar_Producto,
    Revisar_JSON_Editar_Producto_Parcial
)
from core.exceptions import RecursoNoEncontradoError, RecursoDuplicadoError 

logger = logging.getLogger("ProductosService")  

class ProductosService():
    
    @staticmethod
    def crear_producto(db: Session, json: Revisar_JSON_Crear_Producto):
        check = repo.revisar_duplicados_codigo(db, json.codigo)
        
        if check is not None:
            logger.warning(f"Intento crear producto con codigo duplicado: {json.codigo}")  
            raise RecursoDuplicadoError("Producto con este codigo ya esta registrado")
        
        new_product = Productos(
            nombre=json.nombre,
            stock=json.stock,
            codigo=json.codigo
        )
        result = repo.crear_nuevo_producto(db, new_product)
        logger.info(f"Producto creado: ID={result.id}, Código={result.codigo}")  
        return result

    @staticmethod
    def obtener_productos_service(db: Session, salto: int, limite: int):
        resultado = repo.obtener_productos(db, salto, limite)
        
        if resultado is None:
            logger.info("No hay productos registrados")  # AGREGADO
            raise RecursoNoEncontradoError("No hay productos registrados")
        else:
            logger.info(f"Obtenidos {len(resultado['data'])} productos, página {resultado['pagina_actual']}")  #
            return resultado
        
    
    @staticmethod
    def editar_producto(db: Session, json: Revisar_JSON_Editar_Producto, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            logger.warning(f"Intento actualizar producto inexistente: ID={id}")  
            raise RecursoNoEncontradoError("No se encontro el recurso")
            
        check.nombre = json.nombre
        check.stock = json.stock
        check.codigo = json.codigo
        result = repo.guardar_cambios_put(db, check)
        logger.info(f"Producto actualizado: ID={id}")  #
        return result

    @staticmethod
    def editar_producto_parcial(db: Session, json: Revisar_JSON_Editar_Producto_Parcial, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            logger.warning(f"Intento actualizar parcialmente producto inexistente: ID={id}")  
            raise RecursoNoEncontradoError("No se encontro el recurso")
        
        datos_actualizar = json.model_dump(exclude_unset=True)
        for campo, valor in datos_actualizar.items():
            setattr(check, campo, valor)
            
        result = repo.guardar_cambios_patch(db, check)
        logger.info(f"Producto actualizado parcialmente: ID={id}")  
        return result

    @staticmethod
    def eliminar_producto(db: Session, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            logger.warning(f"Intento eliminar producto inexistente: ID={id}")  
            raise RecursoNoEncontradoError("No se encontro el recurso")
            
        repo.eliminar_producto(db, check)
        logger.info(f"Producto eliminado: ID={id}")  
        return None