from sqlalchemy import Integer, String, Column
from database.almacen import miclaseBase

class Productos (miclaseBase):
    __tablename__ = "Productos"
    
    id = Column(Integer, primary_key= True, index = True)
    nombre = Column(String, nullable = False)
    stock = Column(Integer, nullable = False)
    codigo = Column(String, unique = True, nullable = False)
    
    
    
    
    
    