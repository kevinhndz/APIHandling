from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from database.almacen import miclaseBase
from database.base import PoderAuditor

class Clients(miclaseBase, PoderAuditor):
    __tablename__ = "Clients"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    # fk's
    id_user = Column(Integer, ForeignKey("Users.id"))
    usuario = relationship("Users", back_populates="clients")
    

