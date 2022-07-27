from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Role(Base):
    __tablename__ = "role"
    id_role = Column(Integer, primary_key=True)
    name = Column(String(20))

class User(Base):
    __tablename__ = "user"
    id_user = Column(Integer, primary_key=True)
    username = Column(String(45), unique=True)
    email = Column(String(50))
    password = Column(String(120))
    id_role = Column(Integer, ForeignKey("role.id_role"))
    role = relationship("Role", backref="user")

class Equipo(Base):
    __tablename__ = "equipo"
    id_equipo = Column(Integer, primary_key=True)
    descripcion = Column(String(45))

class Pais(Base):
    __tablename__ = "pais"
    id_pais = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    name = Column(String(50))
    continente = Column(String(45))
    codigoISO2 = Column(String(2))
    codigoISO3 = Column(String(3))

class Perfil(Base):
    __tablename__ = "perfil"
    id_perfil = Column(Integer, primary_key=True)
    descripcion = Column(String(45))
    jugadores = relationship('Jugador', secondary='jugador_perfil', back_populates='perfiles')

class Pie(Base):
    __tablename__ = "pie"
    id_pie = Column(Integer, primary_key=True)
    descripcion = Column(String(15))

class Posicion(Base):
    __tablename__ = "posicion"
    id_posicion = Column(Integer, primary_key=True)
    descripcion = Column(String(30))

class Seguimiento(Base):
    __tablename__ = "seguimiento"
    id_seguimiento = Column(Integer, primary_key=True)
    descripcion = Column(String(45))

class Somatotipo(Base):
    __tablename__ = "somatotipo"
    id_somatotipo = Column(Integer, primary_key=True)
    descripcion = Column(String(45))

class Visualizacion(Base):
    __tablename__ = "visualizacion"
    id_visualizacion = Column(Integer, primary_key=True)
    descripcion = Column(String(10))
    
jugador_perfil = Table(
    "jugador_perfil",
    Base.metadata,
    Column("id_jugador", ForeignKey("jugador.id_jugador"), primary_key=True),
    Column("id_perfil", ForeignKey("perfil.id_perfil"), primary_key=True)
)

class Jugador(Base):
    __tablename__ = "jugador"
    id_jugador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(120))
    apodo = Column(String(120))
    anio = Column(Integer)
    id_equipo = Column(Integer, ForeignKey("equipo.id_equipo"))
    numero = Column(Integer)
    id_pie = Column(Integer, ForeignKey("pie.id_pie"))
    id_somatotipo = Column(Integer, ForeignKey("somatotipo.id_somatotipo"))
    estatura = Column(Integer)
    id_pais = Column(Integer, ForeignKey("pais.id_pais"))
    id_pais_nacionalidad = Column(Integer, ForeignKey("pais.id_pais"))
    id_posicion1 = Column(Integer, ForeignKey("posicion.id_posicion"))
    id_posicion2 = Column(Integer, ForeignKey("posicion.id_posicion"))
    
    equipo = relationship("Equipo", backref="jugador")
    pie = relationship("Pie", backref="jugador")
    somatotipo = relationship("Somatotipo", backref="jugador")
    pais = relationship("Pais", foreign_keys=[id_pais], backref="jugador")
    nacionalidad = relationship("Pais", foreign_keys=[id_pais_nacionalidad], backref="jugador.id_pais_nacionalidad")
    posicion1 = relationship("Posicion", foreign_keys=[id_posicion1], backref="jugador")
    posicion2 = relationship("Posicion", foreign_keys=[id_posicion2], backref="jugador.id_posicion2")

    perfiles = relationship("Perfil", secondary='jugador_perfil', back_populates="jugadores")
    valoraciones = relationship("Valoracion", back_populates="jugadores")

class Valoracion(Base):
    __tablename__ = "valoracion"
    id_valoracion = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id_user"))
    fecha  = Column(DateTime)
    id_visualizacion = Column(Integer, ForeignKey("visualizacion.id_visualizacion"))
    id_equipo = Column(Integer, ForeignKey("equipo.id_equipo"))
    local = Column(Integer, ForeignKey("equipo.id_equipo"))
    visitante = Column(Integer, ForeignKey("equipo.id_equipo"))
    campeonato = Column(String(100))
    id_seguimiento = Column(Integer, ForeignKey("seguimiento.id_seguimiento"))
    descripcion = Column(String(1000))
    id_jugador = Column(Integer, ForeignKey("jugador.id_jugador"))
    active = Column(String(1), default='Y')
    user = relationship("User", backref="valoracion")
    visualizacion = relationship("Visualizacion", backref="valoracion")
    equipo = relationship("Equipo", foreign_keys=[id_equipo], backref="valoracion.id_equipo")
    equipo_local = relationship("Equipo", foreign_keys=[local], backref="valoracion.local")
    equipo_visitante = relationship("Equipo", foreign_keys=[visitante], backref="valoracion.visitante")
    seguimiento = relationship("Seguimiento", backref="valoracion")    
    jugadores = relationship("Jugador", backref="jugadores")