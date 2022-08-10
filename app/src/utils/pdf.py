from fpdf import FPDF

from app.src.data.orm import Jugador, User
import locale

class PDF(FPDF):
    def header(self):
        # Logo
        #self.image('logo_pb.png', 10, 8, 33)
        # title = '{} - Informe de jugador'.format(title)
        # Arial bold 15
        self.set_font('Arial', '', 12)
        # Move to the right
        self.set_x(-30 -len(self.title))
        # Title
        self.cell(30, 10, self.title, 0, 0, 'C')
        # Line break
        self.ln(20)
        
    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

class JugadorInforme():
    def create_informe(self, user: User, jugador: Jugador, valoraciones):
        locale.setlocale(locale.LC_TIME, 'es_ES')
        pdf = PDF()
        pdf.set_title('{} - Informe de jugador'.format(user.username))
        self.create_body(pdf, jugador, valoraciones)
        return pdf
        
    def create_body(self, pdf: PDF, jugador: Jugador, valoraciones):        
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 15)
        pdf.cell(0, 10, jugador.nombre, 0, 1)
        
        pdf.set_font('Times', '', 12)
        self.multi_cell(pdf, [  [80,10,str(jugador.anio),0,0],
                                [40,10,jugador.pais.nombre,0,0]])
        
        self.multi_cell(pdf, [  [80,10,'{} cm'.format(jugador.estatura),0,0],
                                [40,10,jugador.somatotipo.descripcion
                                 if jugador.somatotipo else '',0,0]])
        
        self.multi_cell(pdf, [  [80,10,'{}, {}'.format(jugador.posicion1.descripcion
                                                       if jugador.posicion1 else '', 
                                                       jugador.posicion2.descripcion
                                                       if jugador.posicion2 else ''),0,0],
                                [40,10, jugador.pie.descripcion
                                 if jugador.pie else '',0,0]])
        
        pdf.cell(0, 10, ', '.join(map(str, map(lambda perfil: perfil.descripcion, jugador.perfiles))), 0, 1)
        
        self.create_valoraciones(pdf, valoraciones)

    
    def create_valoraciones(self, pdf: PDF, valoraciones):
        pdf.ln(20)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Valoraciones', 0, 1)
        pdf.set_font('Times', '', 12)
        for valoracion in valoraciones:
            pdf.ln(3)
            pdf.dashed_line(10, pdf.y, 180, pdf.y, 1, 0)
            pdf.ln(3)
            self.draw_rect_seguimiento(pdf, valoracion.id_seguimiento)
            pdf.set_x(16)
            pdf.cell(0, 10, '{} - {}'\
                .format(''.join(map(lambda word: word[0], valoracion.user.username.split(" "))),\
                valoracion.fecha.strftime("%d %B %Y")), 0, 1)
            pdf.ln(5)
            pdf.cell(0, 5, '{} - {}'.format(valoracion.equipo_local.descripcion, valoracion.equipo_visitante.descripcion), 0, 1)
            pdf.cell(0, 5, valoracion.campeonato, 0, 1)
            pdf.ln(5)
            self.multi_cell(pdf, [  [200,5,'{}'.format(valoracion.descripcion),0,0]])

    def draw_rect_seguimiento(self, pdf: PDF, id_seguimiento):
        rgb_seg =           {1: [0,   0,   0],
                             2: [0,   255, 0],
                             3: [255, 255, 0],
                             4: [128, 0,   255],
                             5: [0,   0,   255],
                             6: [93, 173, 226],
                             7: [153, 102, 0],
                             8: [255, 128, 0],
                             9: [255, 0, 0],
                             10: [255, 255, 255]
        }
        pdf.set_fill_color(r=rgb_seg[id_seguimiento][0], g=rgb_seg[id_seguimiento][1], b=rgb_seg[id_seguimiento][2])
        pdf.rect(x=pdf.x, y=pdf.y+2, w=6, h=6, style="FD")
        
    def multi_cell(self, pdf, cells):
        x = pdf.x
        max_y = 0
        for cell in cells:
            top = pdf.y
            offset = pdf.x + cell[0]
            pdf.multi_cell(cell[0],cell[1],cell[2],cell[3],cell[4])
            max_y = pdf.y if pdf.y > max_y else max_y
            pdf.y = top
            pdf.x = offset 
        pdf.y = max_y
        pdf.ln(2)
        
        
