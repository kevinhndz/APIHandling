from fastapi.testclient import TestClient
from main import app

# Instanciamos el robot cliente de pruebas
robot = TestClient(app)

def test_login_credenciales_invalidas():
    respuesta = robot.post(
        "/login/",
        json={"user": "usuario_falso", "password": "contrasena_falsa"}
    )
    
    datos = respuesta.json()
    
    assert respuesta.status_code == 401
    assert datos["detail"] == "Usuario o contraseña incorrectos"
    
    print("\n--- PRUEBA 1: CREDENCIALES INVALIDAS ---")
    print("STATUS CODE:", respuesta.status_code)
    print("JSON DEVUELTO:", datos)


def test_login_exitoso():
    respuesta = robot.post(
        "/login/",
        json={"user": "kevstpg", "password": "Realforever11"}
    )
    
    datos = respuesta.json()
    
    assert respuesta.status_code == 200
    assert "token" in datos
    assert datos["user"] == "kevstpg"
    
    print("\n--- PRUEBA 2: LOGIN EXITOSO ---")
    print("STATUS CODE:", respuesta.status_code)
    print("JSON DEVUELTO:", datos)