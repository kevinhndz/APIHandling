from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from core.exceptions import (
    RecursoNoEncontradoError, 
    RecursoDuplicadoError,
    CredencialesInvalidasError,
    AccesoProhibidoError
)


class ExcepcionesGlobales:

    @staticmethod
    def recurso_no_encontrado(request: Request, exc: RecursoNoEncontradoError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.mensaje}
        )

    @staticmethod
    def recurso_duplicado(request: Request, exc: RecursoDuplicadoError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.mensaje}
        )

    @staticmethod
    def credenciales_invalidas(request: Request, exc: CredencialesInvalidasError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.mensaje}
        )

    @staticmethod
    def acceso_prohibido(request: Request, exc: AccesoProhibidoError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": exc.mensaje}
        )

    @classmethod
    def registrar_handlers(cls, app: FastAPI) -> None:
        """Registra automaticamente todos los manejadores en la instancia de FastAPI."""
        app.add_exception_handler(RecursoNoEncontradoError, cls.recurso_no_encontrado)
        app.add_exception_handler(RecursoDuplicadoError, cls.recurso_duplicado)
        app.add_exception_handler(CredencialesInvalidasError, cls.credenciales_invalidas)
        app.add_exception_handler(AccesoProhibidoError, cls.acceso_prohibido)