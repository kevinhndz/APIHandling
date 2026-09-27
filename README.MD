OPTIMIZACIONES DEL SISTEMA:


OPTIMIZACION #1:

QUIEN ES QUIEN

- BaseSettings es una clase "mágica" que sabe cómo buscar variables de entorno automáticamente. (reemplaza los ifs)

- SettingsConfigDict es un diccionario especial que le da instrucciones a BaseSettings sobre cómo 
comportarse (por ejemplo, decirle qué archivo leer).

¿Cómo se comunican estos archivos con core/config.py?
Fase de inicio (Milisegundo 0): Cuando inicias tu servidor Uvicorn, Python procesa los archivos. Al llegar a core/config.py, ejecuta la línea settings = Settings(). En ese momento, Pydantic lee el .env y guarda en memoria RAM los valores de DATABASE_URL, SECRET_KEY, ALGORITHM, etc.

Petición en almacen.py: Al ejecutar UBICACION_ALMACEN = settings.DATABASE_URL, almacen.py no abre ningún archivo ni usa el sistema operativo (os). Simplemente consulta el atributo .DATABASE_URL del objeto settings que ya fue validado en la memoria.

Petición en token.py: Al ejecutar KEY = settings.SECRET_KEY, este archivo le pide al objeto settings la clave secreta. Si necesitas cambiar el algoritmo en el futuro, settings.ALGORITHM se encargará de entregar "HS256" de forma centralizada sin necesidad de escribir la cadena de texto a mano dentro de cada función.