from fastapi import FastAPI , HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database.almacen import abrir_puerta, miclaseBase, motor
from modules.productos.model import Productos
from modules.productos.schema import Revisar_JSON_Crear_Producto, Revisar_JSON_Editar_Producto

app = FastAPI()

miclaseBase.metadata.create_all(bind = motor)

router = APIRouter(
    prefix = "/productos",
    tags = ["Productos"]
)

#PROTOTIPO DE POST


@router.post("/", status_code= 201)
def crear_producto(json: Revisar_JSON_Crear_Producto,
                   db:Session = Depends(abrir_puerta)
                   ):
    
    check = db.query(Productos).filter(Productos.codigo == json.codigo).first()
    
    if check is not None:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"El producto con codigo {json.codigo} ya existe"
        )
    else:
        nuevo = Productos(
            nombre = json.nombre,
            stock = json.stock,
            codigo = json.codigo
        )
        
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {"Mensaje": f"Producto: {nuevo.nombre} con ID : {nuevo.id} creado exitosamente"}
    
    
    
#PROTOTIPO DE GET:

@router.get("/")
def ver_productos (limite: int = 10, salto: int = 0 ,db: Session = Depends (abrir_puerta)):
    
    check = db.query(Productos).offset(salto).limit(limite).all()
    
    if not check:
        raise HTTPException(
            satus_code = status.HTTP_404_NOT_FOUND,
            detail = "No records found!"
        )
    else:
        return check
    

@router.put("/{id}")
def editar_producto(
    id: int, 
    json: Revisar_JSON_Crear_Producto,  
    db: Session = Depends(abrir_puerta)
):
    check = db.query(Productos).filter(Productos.id == id).first()
    
    if check is not None:
        check.nombre = json.nombre
        check.codigo = json.codigo
        check.stock = json.stock
        
        db.commit()
        db.refresh(check)
        
        return check  
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
        
        
@router.patch("/{id}")
def editar_producto_parcial(
    id: int, 
    json: Revisar_JSON_Editar_Producto,  
    db: Session = Depends(abrir_puerta)
):
    check = db.query(Productos).filter(Productos.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    # 1. Convertimos el JSON a diccionario, ignorando los campos que no se enviaron
    datos_a_actualizar = json.model_dump(exclude_unset=True)
    
    # 2. Actualizamos solo las columnas que llegaron en la peticion
    for clave, valor in datos_a_actualizar.items():
        setattr(check, clave, valor)
        
    db.commit()
    db.refresh(check)
    
    return check


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def borrar_producto(
    id: int, 
    db: Session = Depends(abrir_puerta)
):
  
    check = db.query(Productos).filter(Productos.id == id).first()
    
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    db.delete(check)
    db.commit()
    
    return {"mensaje": f"El producto con ID {id} fue eliminado correctamente"}