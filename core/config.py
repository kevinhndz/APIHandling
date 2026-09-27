from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Declaramos las variables exactas del .env
    DATABASE_URL: str
    SECRET_KEY: str
    
    # Declaramos variables extra que va ocupar JWT, con valores por defecto
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20

    # Le decimos de donde leer la informacion
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Creamos una unica instancia para todo el proyecto
settings = Settings()

