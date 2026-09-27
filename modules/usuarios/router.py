from fastapi import FastAPI , HTTPException , status, Depends, APIRouter
from sqlalchemy.orm import Session
from database.almacen import abrir_puerta
from modules.usuarios.schema import Revisar_JSON_Login
from modules.usuarios.model import Users
from utils.hash import verificar_contrasena
from utils.token import crear_token
from modules.usuarios.service import UsuarioService as service

router = APIRouter(
    prefix = "/login",
    tags = ["Login"]
)

#json waiting
@router.post("/")
def login(json: Revisar_JSON_Login, db: Session = Depends(abrir_puerta)):
    return service.login_service(db, json)

    
        
    
       
