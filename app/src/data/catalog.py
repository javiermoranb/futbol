from app.src.data.orm import Pais
import app.src.utils.constants as c
from app.src.utils.utils import Utils
from sqlalchemy import or_



#creates db
def get_catalog(db, obj, id_col, args):    
    query = db.session.query(obj)
    if c.URL_PARAM_ID in args:
        query = query.filter(obj.__table__.c[id_col]  == args[c.URL_PARAM_ID]).first()
    else:
        if c.URL_PARAM_DESCRIPCION in args:
            search1 = f"{args[c.URL_PARAM_DESCRIPCION]}%"
            search2 = f"% {args[c.URL_PARAM_DESCRIPCION]}%"
            query = query.filter(or_(obj.descripcion.ilike(search1), obj.descripcion.ilike(search2)))
            print(str(query))
            
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