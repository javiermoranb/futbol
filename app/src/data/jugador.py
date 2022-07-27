from app.src.data.orm import Jugador
import app.src.utils.constants as c
from app.src.utils.mapper import Mapper

def get_jugador(db, args):
    query = db.session.query(Jugador)
    result = None
    if c.URL_PARAM_ID in args:
        result = query.filter_by(id_jugador = args[c.URL_PARAM_ID]).first()
    elif c.URL_PARAM_NOMBRE in args:
        search = "{}%".format(args[c.URL_PARAM_NOMBRE])
        result = query.filter(Jugador.nombre.ilike(search))\
            .order_by(Jugador.nombre).all()
    else:
        result = query.order_by(Jugador.nombre).all()
    
    return result
        

def insert_jugador(db, data_jugador):
    #id_jugador = db.session.query(func.max(Jugador.id_jugador)).first()
    #data_jugador['id_jugador']  = id_jugador._data[0]+1
    newJugador = Mapper().map_json_as_jugador(db, data_jugador)
    
    db.session.add(newJugador)
    db.session.commit()
    return Mapper().map_min_jugador_as_json(newJugador)
    

def update_jugador(db, data_jugador):    
    perfiles = data_jugador['perfiles']
    del data_jugador['perfiles']
    db.session.query(Jugador).filter(Jugador.id_jugador == data_jugador['id_jugador']).\
    update(data_jugador, synchronize_session='fetch')

    
    db.session.commit()
    jugador = db.session.query(Jugador).filter_by(id_jugador = data_jugador['id_jugador']).first()
    Mapper().add_jugador_perfil(db, jugador, perfiles)
    db.session.commit()

    return {'text': 'Jugador editado'}