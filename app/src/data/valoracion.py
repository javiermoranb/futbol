import app.src.utils.constants as c
from app.src.data.orm import Valoracion
from app.src.utils.mapper import Mapper


def get_valoracion(db, user, args):
    query = db.session.query(Valoracion)\
        .filter_by(id_jugador = args[c.URL_PARAM_ID_JUGADOR])\
        .filter_by(active = c.ACTIVE_YES)
    
    if user.id_role != 3:
        query = query.filter_by(id_user = user.id_user)
    
    
    if c.URL_PARAM_ID_VALORACION in args:
        query = query.filter(Valoracion.id_valoracion.in_([1,3]))
    
    result = query.order_by(Valoracion.fecha.desc()).all()
    return result


def insert_valoracion(db, data_valoracion):

    newValoracion = Mapper().map_json_as_valoracion(data_valoracion)
    
    db.session.add(newValoracion)
    db.session.commit()

    return {'text': 'Valoración insertada'}


def soft_delete_valoracion(db, id_valoracion):    
    db.session.query(Valoracion).filter(Valoracion.id_valoracion == id_valoracion).\
    update({'active': c.ACTIVE_NO})
    
    db.session.commit()

    return {'text': 'Valoración insertada'}