from sqlalchemy.orm import Session
from modules.productos.model import Productos

class ProductosRepository():
    
    @staticmethod
    def revisar_duplicados_codigo(db: Session, codigo: str) -> dict:
        check = db.query(Productos).filter(Productos.codigo == codigo).first()
        return check
        
    @staticmethod
    def crear_nuevo_producto(db: Session, new_product: dict) -> dict:
        db.add(new_product)
        db.commit()          
        db.refresh(new_product) 
        return new_product

    @staticmethod
    def obtener_productos_paginados(db: Session, salto: int, limite: int):
        return db.query(Productos).offset(salto).limit(limite).all()

    @staticmethod
    def buscar_por_id(db: Session, id: int):
        return db.query(Productos).filter(Productos.id == id).first()
    
    @staticmethod
    def guardar_cambios_put(db: Session, producto_editado: dict) -> dict:
        db.commit()
        db.refresh(producto_editado)
        return producto_editado

    @staticmethod
    def guardar_cambios_patch(db: Session, producto: Productos) -> Productos:
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def eliminar_producto(db: Session, producto: Productos) -> None:
        db.delete(producto)
        db.commit()