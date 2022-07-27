from app.src.data.orm import Pais
import app.src.utils.constants as c
from app.src.utils.utils import Utils



#creates db
def get_catalog(db, obj, id_col, args):    
    result = None
    query = db.session.query(obj)
    if c.URL_PARAM_ID in args:
        result = query.filter(obj.__table__.c[id_col]  == args[c.URL_PARAM_ID]).first()
    elif c.URL_PARAM_DESCRIPCION in args:
        search = "{}%".format(args[c.URL_PARAM_DESCRIPCION])
        result = query.filter(obj.descripcion.ilike(search))\
            .order_by(obj.descripcion).all()
    else:
        result = query.order_by(obj.descripcion).all()
    
    return Utils().orm_to_json(result)

def get_paises(db, args):
    result = None
    query = db.session.query(Pais)
    if c.URL_PARAM_ID in args:
        result = query.filter(id_pais  = args[c.URL_PARAM_ID]).first()
    elif c.URL_PARAM_NOMBRE in args:
        search = "{}%".format(args[c.URL_PARAM_NOMBRE])
        result = query.filter(Pais.nombre.ilike(search))\
            .order_by(Pais.nombre).all()
    else:
        result = query.order_by(Pais.nombre).all()
    
    return Utils().orm_to_json(result)