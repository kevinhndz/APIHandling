from fastapi import Header,Depends, HTTPException, status
from utils.token import verificar_token

def el_vigilante(token: str = Header(...)) -> dict:
    return verificar_token(token)


def permiso_admin (json: dict = Depends(el_vigilante)) -> dict:
    
    if json["rol"] != "Admin":
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail = "No estas autorizado")
    else:
        return json
    
def permiso_usuario (json: dict = Depends(el_vigilante)) -> dict:
    
    if json["rol"] not in ["Usuario", "Admin"]:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, 
                            detail = "No estas autorizado")
    else:
        return json