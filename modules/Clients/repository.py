from sqlalchemy.orm import Session
from modules.Clients.model import Clients

class ClientsRepository():
    
    @staticmethod
    def revisar_duplicados(db: Session, json: dict) -> dict:
        check = db.query(Clients).filter(Clients.email == json.email).first()
        return check
        
    @staticmethod
    def crear_nuevo_user(db: Session, new_user: dict) -> dict:
        db.add(new_user)
        db.commit()          
        db.refresh(new_user) 
        return new_user
    
    @staticmethod
    def crear_nuevo_customer(db: Session, new_customer: dict) -> dict:
        db.add(new_customer)
        db.commit()         
        db.refresh(new_customer)
        return new_customer

    @staticmethod
    def obtener_clientes_paginados(db: Session, salto: int, limite: int):
        return db.query(Clients).offset(salto).limit(limite).all()
    
    @staticmethod
    def revisar_duplicados_por_ID_put(db: Session, id: int) -> dict:
        check = db.query(Clients).filter(Clients.id == id).first()
        return check
    
    @staticmethod
    def guardar_cambios_put(db: Session, cliente_editado: dict) -> dict:
        db.commit()
        db.refresh(cliente_editado)
        return cliente_editado

    @staticmethod
    def buscar_por_id(db: Session, id: int):
        return db.query(Clients).filter(Clients.id == id).first()

    @staticmethod
    def guardar_cambios_patch(db: Session, cliente: Clients) -> Clients:
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def eliminar_cliente(db: Session, cliente: Clients) -> None:
        db.delete(cliente)
        db.commit()


