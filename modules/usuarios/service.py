from sqlalchemy.orm import Session
from modules.usuarios.schema import Revisar_JSON_Login
from utils.hash import verificar_contrasena
from utils.token import crear_token
from modules.usuarios.repository import UsuariosRepository as repo
from core.exceptions import CredencialesInvalidasError

class UsuarioService():
    
    @staticmethod
    def login_service(db: Session, json: Revisar_JSON_Login):
        
        check = repo.revisar(db, json)
        
        if check is None or not verificar_contrasena(json.password, check.password):
            raise CredencialesInvalidasError("Usuario o contraseña incorrectos")
        else:
            token = crear_token(check.id, check.user, check.rol)
            return {"user": check.user, "id_user": check.id, "token": token}