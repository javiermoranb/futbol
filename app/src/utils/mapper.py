from flask import jsonify

from app.src.data.orm import Jugador, Perfil, Valoracion

class Mapper:

    def map_min_jugador_as_json(self, jugador):
        return jsonify({'jugador':
                    {
                        'id_jugador': jugador.id_jugador,
                        'nombre' : jugador.nombre
                    }
                })

    def map_jugador_as_json(self, result):
        if isinstance(result, list):
            output = []
            for jugador in result:
                # appending the user data json 
                # to the response list
                output.append({
                    'id_jugador': jugador.id_jugador,
                    'nombre' : jugador.nombre
                })

            return jsonify({'jugadores': output})
        else:
            jugador = result
            return jsonify({'jugador':
                    {
                        'id_jugador': jugador.id_jugador,
                        'nombre' : jugador.nombre,
                        'apodo' : jugador.apodo,
                        'anio' : jugador.anio,
                        'equipo' : {
                            'id_equipo': jugador.equipo.id_equipo,
                            'descripcion': jugador.equipo.descripcion
                        },
                        'numero' : jugador.numero,
                        'pie' : {
                            'id_pie': jugador.pie.id_pie,
                            'descripcion': jugador.pie.descripcion
                        } if jugador.pie else '',
                        'somatotipo' : {
                            'id_somatotipo': jugador.somatotipo.id_somatotipo,
                            'descripcion': jugador.somatotipo.descripcion
                        } if jugador.somatotipo else '',
                        'estatura' : jugador.estatura,
                        'pais' : {
                            'id_pais': jugador.pais.id_pais,
                            'nombre': jugador.pais.nombre
                        },
                        'nacionalidad' : {
                            'id_pais': jugador.nacionalidad.id_pais,
                            'nombre': jugador.nacionalidad.nombre
                        } if jugador.nacionalidad else '',
                        'posicion1' : {
                            'id_posicion': jugador.posicion1.id_posicion,
                            'descripcion': jugador.posicion1.descripcion
                        },
                        'posicion2' : {
                            'id_posicion': jugador.posicion2.id_posicion,
                            'descripcion': jugador.posicion2.descripcion
                        } if jugador.posicion2 else '',
                        'perfiles': self.map_jugador_perfil_as_json(jugador)

                    }
                })

    def map_jugador_perfil_as_json(self, jugador):
        output = []
        for perfil in jugador.perfiles:
            # appending the user data json 
            # to the response list
            output.append({
                'id_perfil': perfil.id_perfil,
                'descripcion' : perfil.descripcion
            })
        return output

    def map_json_as_jugador(self, db, data_jugador):
        jugador = Jugador(id_jugador = data_jugador['id_jugador'] if data_jugador['id_jugador']>0 else None,
                        nombre = data_jugador['nombre'],
                        apodo = data_jugador['apodo'],
                        anio = data_jugador['anio'],
                        id_equipo = data_jugador['id_equipo'],
                        numero = data_jugador['numero'] if 'numero' in data_jugador else None,
                        id_pie = data_jugador['id_pie'] if 'id_pie' in data_jugador else None,
                        id_somatotipo = data_jugador['id_somatotipo'] if 'id_somatotipo' in data_jugador else None,
                        estatura = data_jugador['estatura'] if 'estatura' in data_jugador else None,
                        id_pais = data_jugador['id_pais'],
                        id_pais_nacionalidad = data_jugador['id_pais_nacionalidad'] if 'id_pais_nacionalidad' in data_jugador else None,
                        id_posicion1 = data_jugador['id_posicion1'],
                        id_posicion2 =  data_jugador['id_posicion2'] if 'id_posicion2' in data_jugador else None)
        self.add_jugador_perfil(db, jugador, data_jugador['perfiles'])
        return jugador
        

    def add_jugador_perfil(self, db, jugador, perfiles):
        jugador.perfiles = []
        for perfil in perfiles:
            jugador.perfiles.append(db.session.query(Perfil).filter(Perfil.id_perfil  == perfil).first())
            
            
            
    def map_valoracion_as_json(self, result):
        output = []
        for valoracion in result:
            # appending the user data json 
            # to the response list
            output.append({
                'id_valoracion': valoracion.id_valoracion,
                'fecha': valoracion.fecha,
                'scout': {
                    'id' : valoracion.user.id_user,
                    'nombre': valoracion.user.username
                },
                'visualizacion': {
                    'id_visualizacion': valoracion.visualizacion.id_visualizacion,
                    'descripcion': valoracion.visualizacion.descripcion
                },
                'campeonato': valoracion.campeonato,
                'equipo': {
                    'id_equipo': valoracion.equipo.id_equipo,
                    'descripcion': valoracion.equipo.descripcion
                },
                'equipo_local': {
                    'id_equipo': valoracion.equipo_local.id_equipo,
                    'descripcion': valoracion.equipo_local.descripcion
                },
                'equipo_visitante': {
                    'id_equipo': valoracion.equipo_visitante.id_equipo,
                    'descripcion': valoracion.equipo_visitante.descripcion
                },
                'seguimiento': {
                    'id_seguimiento': valoracion.seguimiento.id_seguimiento,
                    'descripcion': valoracion.seguimiento.descripcion
                }
                
                
                
            })
        return jsonify({'valoraciones': output} if isinstance(result, list) else {'valoracion': output[0]})
       
       
    def map_json_as_valoracion(self, data_valoracion):
        valoracion = Valoracion(id_valoracion = data_valoracion['id_valoracion'] if data_valoracion['id_valoracion']>0 else None,
                        id_user = data_valoracion['id_user'],
                        fecha = data_valoracion['fecha'],
                        id_visualizacion = data_valoracion['id_visualizacion'],
                        id_equipo = data_valoracion['id_equipo'],
                        local = data_valoracion['id_local'],
                        visitante = data_valoracion['id_visitante'],
                        campeonato = data_valoracion['campeonato'],
                        id_seguimiento = data_valoracion['id_seguimiento'],
                        descripcion = data_valoracion['descripcion'],
                        id_jugador = data_valoracion['id_jugador'],)
        return valoracion