from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from modules.productos.repository import ProductosRepository as repo
from modules.productos.model import Productos
from modules.productos.schema import (
    Revisar_JSON_Crear_Producto, 
    Revisar_JSON_Editar_Producto,
    Revisar_JSON_Editar_Producto_Parcial
)

class ProductosService():
    
    @staticmethod
    def crear_producto(db: Session, json: Revisar_JSON_Crear_Producto):
        check = repo.revisar_duplicados_codigo(db, json.codigo)
        
        if check is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Producto con este codigo ya esta registrado"
            )
        else:
            new_product = Productos(
                nombre=json.nombre,
                stock=json.stock,
                codigo=json.codigo
            )
            
            return repo.crear_nuevo_producto(db, new_product)

    @staticmethod
    def obtener_productos(db: Session, salto: int, limite: int):
        return repo.obtener_productos_paginados(db, salto, limite)
    
    @staticmethod
    def editar_producto(db: Session, json: Revisar_JSON_Editar_Producto, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is not None:
            check.nombre = json.nombre
            check.stock = json.stock
            check.codigo = json.codigo
            editado = repo.guardar_cambios_put(db, check)
            return editado
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro el recurso"
            )

    @staticmethod
    def editar_producto_parcial(db: Session, json: Revisar_JSON_Editar_Producto_Parcial, id: int):
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
    def eliminar_producto(db: Session, id: int):
        check = repo.buscar_por_id(db, id)
        
        if check is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro el recurso"
            )
            
        repo.eliminar_producto(db, check)
        return None