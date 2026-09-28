from pydantic import BaseModel, Field
from typing import Optional

class Revisar_JSON_Crear_Producto(BaseModel):
    nombre: str = Field(min_length=3, max_length=25)
    stock: int = Field(ge=0)
    codigo: str

class Revisar_JSON_Editar_Producto(BaseModel):
    nombre: str = Field(min_length=3, max_length=25)
    stock: int = Field(ge=0)
    codigo: str

class Revisar_JSON_Editar_Producto_Parcial(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=25)
    stock: Optional[int] = Field(None, ge=0)
    codigo: Optional[str] = None
    
class ProductoRespuesta(BaseModel):
    id: int
    nombre: str
    stock: int
    codigo: str

    class Config:
        from_attributes = True