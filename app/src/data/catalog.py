from app.src.data.orm import Pais
import app.src.utils.constants as c
from app.src.utils.utils import Utils



#creates db
def get_catalog(db, obj, id_col, args):    
    query = db.session.query(obj)
    if c.URL_PARAM_ID in args:
        query = query.filter(obj.__table__.c[id_col]  == args[c.URL_PARAM_ID]).first()
    else:
        if c.URL_PARAM_DESCRIPCION in args:
            search = "{}%".format(args[c.URL_PARAM_DESCRIPCION])
            query = query.filter(obj.descripcion.ilike(search))
            
        if c.URL_PARAM_ORDER_BY in args and args[c.URL_PARAM_ORDER_BY]==c.URL_PARAM_ID:
            query = query.order_by(obj.__table__.c[id_col]).all()
        else:
            query = query.order_by(obj.descripcion).all()
    
    return Utils().orm_to_json(query)

def get_paises(db, args):
    query = db.session.query(Pais)
    if c.URL_PARAM_ID in args:
        query = query.filter(id_pais  = args[c.URL_PARAM_ID]).first()
    elif c.URL_PARAM_NOMBRE in args:
        search = "{}%".format(args[c.URL_PARAM_NOMBRE])
        query = query.filter(Pais.nombre.ilike(search))\
            .order_by(Pais.nombre).all()
    else:
        query = query.order_by(Pais.nombre).all()
    
    return Utils().orm_to_json(query)