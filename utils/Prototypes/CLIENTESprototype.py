from fastapi import FastAPI , HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database.almacen import abrir_puerta, miclaseBase, motor
from modules.Clients.model import Clients
from modules.usuarios.model import Users
from utils.hash import encriptar_contrasena
from modules.Clients.schema import(
    
    Revisar_JSON_Crear_Nuevo_Cliente, 
    Revisar_JSON_Editar_Cliente,
    Revisar_JSON_Editar_Cliente_Parcial
)


router = APIRouter(
    prefix = "/clients",
    tags = ["Clients"]
)

@router.post("/")
def crear_nuevo_cliente(json: Revisar_JSON_Crear_Nuevo_Cliente,
                        db: Session = Depends(abrir_puerta)
                        ):
    
    check = db.query(Clients).filter(Clients.email == json.email).first()
    
    if check is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Cliente ya esta registrado"
        )
    else:
        
        new_user = Users(
            
            user = json.user,
            password = encriptar_contrasena(json.password),
            rol = json.rol
        )
        
        db.add(new_user)
        db.refresh(new_user)
        
        new_customer = Clients(
            nombre = json.nombre,
            email = json.email,
            id_user = new_user.id
        )
        
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
        
        
@router.put("/{id}")
def editar(id: int, json: Revisar_JSON_Editar_Cliente, db: Session = Depends(abrir_puerta)):
    
    check = db.query(Clients).filter(Clients.id == id).first()
    
    if check is not None:
        check.nombre = json.nombre
        check.email = json.email
        db.commit()
        db.refresh(check)
        return check
    else:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "No se encontro el recurso"
        )
        
@router.patch("/{id}")
def editar_parcial(
    id: int, 
    json: Revisar_JSON_Editar_Cliente_Parcial, 
    db: Session = Depends(abrir_puerta)
):
    check = db.query(Clients).filter(Clients.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el recurso"
        )
    
    
    datos_actualizar = json.model_dump(exclude_unset=True)
    
    for campo, valor in datos_actualizar.items():
        setattr(check, campo, valor)
        
    db.commit()
    db.refresh(check)
    return check


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(id: int, db: Session = Depends(abrir_puerta)):
    check = db.query(Clients).filter(Clients.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el recurso"
        )
        
    db.delete(check)
    db.commit()
    return None