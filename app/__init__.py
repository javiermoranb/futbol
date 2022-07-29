import os
import json
import app.src.utils.constants as c

# definición de constantes a usar en la app
LOCAL_PROPERTIES = 'local.properties'

# Variable de entorno
if os.path.isfile(LOCAL_PROPERTIES):
    with open(LOCAL_PROPERTIES) as f:
        for k, v in json.load(f).items():
            os.environ[k] = v