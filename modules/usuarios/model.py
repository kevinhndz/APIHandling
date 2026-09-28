from sqlalchemy import Integer, String, Column, ForeignKey
from database.almacen import miclaseBase
from sqlalchemy.orm import relationship
from database.base import PoderAuditor

class Users (miclaseBase, PoderAuditor):
    
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key= True, index = True)
    user = Column(String, nullable= False,unique = True)
    password = Column(String, nullable = False)
    rol = Column(String, nullable=False)
    clientes = relationship("Cliente", back_populates="usuario")
