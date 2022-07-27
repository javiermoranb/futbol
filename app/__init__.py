import os
import json
from app.src.utils.utils import DocumentDB
import app.src.utils.constants as c

# definición de constantes a usar en la app
LOCAL_PROPERTIES = 'local.properties'

client = None
host = None
database_name = None
username = None
password = None

# Variable de entorno
if os.path.isfile(LOCAL_PROPERTIES):
    with open(LOCAL_PROPERTIES) as f:
        for k, v in json.load(f).items():
            os.environ[k] = v

host = os.environ[c.DB_HOST]
database_name = os.environ[c.DB_NAME]
username = os.environ[c.DB_USER]
password = os.environ[c.DB_PASSWORD]

# se crea la conexión a la base de datos
client = DocumentDB(host, database_name, username, password)