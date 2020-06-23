from reportlab.platypus import PageBreak, PageTemplate, BaseDocTemplate, Paragraph, NextPageTemplate, TableStyle, Image, Spacer
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import Color, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.tables import Table
from reportlab.platypus.frames import Frame
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
import datetime
import os


registerFont(TTFont('Arial', 'ARIAL.ttf'))  # register arial fonts
registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))


# file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE_DIR, 'static\\images\\logo.jpg')
SKF = os.path.join(BASE_DIR, 'static\\images\\skf.jpg')
# datetime constants
MONTHS = (
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre'
)
NOW = datetime.datetime.now()
CURRENT_YEAR = NOW.year
CURRENT_MONTH = NOW.month
CURRENT_DAY = NOW.day
# constants for footer
ADDRESS = 'Calle 9A  No. 54 - 129 Guayabal'
PHONE = 'PBX: (4) 362 00 62'
CELPHONE = 'Cel. 312 296 84 50'
WHATSAPP = 'WhatsApp 301  249 92 84'
WEBSITE = 'www.vibromontajes.com'
EMAIL = 'servicios@vibromontajes.com'
FOOTER_CITY = 'Medellín, Colombia'
# constants for colors
HEADER_FOOTER_GREEN = Color(red=0, green=(102/255), blue=0)
COMPANY_HEADER_BLUE = Color(red=(82/255), green=(139/255), blue=(166/255))
TABLE_BLUE = Color(red=(141/255), green=(179/255), blue=(226/255))
FOOTER_BLUE = Color(red=(84/255), green=(141/255), blue=(212/255))
# constants for paragraph styles
STANDARD = ParagraphStyle(
    name='standard', fontName='Arial', fontSize=10)
STANDARD_CENTER = ParagraphStyle(
    name='standard_center', fontName='Arial', fontSize=10, alignment=1)
STANDARD_HEADER = ParagraphStyle(
    name='standard_header', fontName='Arial', fontSize=10, alignment=2)
STANDARD_JUSTIFIED = ParagraphStyle(
    name='standard_justified', fontName='Arial', fontSize=10, alignment=4)
BLACK_BOLD = ParagraphStyle(
    name='black_bold', fontName='Arial-Bold', fontSize=10)
BLACK_BOLD_CENTER = ParagraphStyle(
    name='black_bold_center', fontName='Arial-Bold', fontSize=10, alignment=1)
BLUE_HEADER = ParagraphStyle(name='blue_hf', fontName='Arial-Bold', fontSize=10,
                             textColor=COMPANY_HEADER_BLUE, alignment=2)
BLUE_FOOTER = ParagraphStyle(name='blue_hf', fontName='Arial-Bold', fontSize=10,
                             textColor=FOOTER_BLUE, alignment=1)
BLACK_SMALL = ParagraphStyle(
    name='black_small', fontName='Arial', fontSize=7, alignment=1)
GREEN_SMALL = ParagraphStyle(
    name='green_small', fontName='Arial', fontSize=7, textColor=HEADER_FOOTER_GREEN, alignment=1)
# footer paragraph lines
LINE_ONE = Paragraph('_' * 80, style=BLUE_FOOTER)
LINE_TWO = Paragraph(
    f'{ADDRESS} {PHONE} {CELPHONE} {WHATSAPP}', style=BLACK_SMALL)
LINE_THREE = Paragraph(
    text=f'{WEBSITE} E-mail: <a href="mailto:{EMAIL}"><font color="blue">{EMAIL}</font></a> {FOOTER_CITY}', style=GREEN_SMALL)
# Frames used for templates
STANDARD_FRAME = Frame(1.6*cm, 2*cm, 18*cm, 26*cm,
                       id='standard')
MACHINE_FRAME = Frame(1.6*cm, 2*cm, 18*cm, 23*cm,
                      id='big_header')


class Flowables(BaseDocTemplate):

    """
    class containing all minor flowables 
    used in the creation of documents.
    """

    def __init__(self, filename, queryset, user, **kwargs):
        super().__init__(filename, **kwargs)
        self.filename = filename
        self.queryset = queryset  # model object that populate pdf
        self.user = user
        self.company = self.user.company
        self.date = self.queryset.first().date
        self.engineer_one = self.queryset.first().engineer_one
        self.engineer_two = self.queryset.first().engineer_two
        self.toc = TableOfContents()
        self.story = []
        self.width = 18 * cm
        self.leftMargin = 1.6 * cm
        self.bottomMargin = 2 * cm
        self.templates = [
            PageTemplate(id='measurement',
                         frames=[MACHINE_FRAME],
                         onPage=self._header_one,
                         onPageEnd=self._footer),
            PageTemplate(id='measurement_two',
                         frames=[STANDARD_FRAME],
                         onPage=self._header_two,
                         onPageEnd=self._footer),
            PageTemplate(id='normal',
                         frames=[STANDARD_FRAME],
                         onPage=self._header_two),
        ]
        self.addPageTemplates(self.templates)

    def _create_header_table(self):
        """
        create table to manage
        elements in custom header.
        """

        logo = Image(LOGO, width=8.65 * cm, height=2.51 * cm)
        skf = Image(SKF, width=1.76 * cm, height=0.47 * cm)
        skf_text = Paragraph('Con tecnología', style=GREEN_SMALL)
        report_date = Paragraph(self.date.upper(), style=STANDARD_HEADER)
        company = Paragraph(self.company.upper(), style=BLUE_HEADER)
        data = [[logo, skf_text, report_date], ['', skf, company]]
        styles = [
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (1, 0), (1, 0), 'BOTTOM'),
            ('VALIGN', (1, -1), (1, -1), 'TOP'),
            ('VALIGN', (2, 0), (2, -1), 'MIDDLE'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('SPAN', (0, 0), (0, -1)),
        ]
        table = Table(
            data,
            colWidths=[
                9 * cm,
                2.5 * cm,
                6.5 * cm],
            rowHeights=[
                1.26 * cm,
                1.26 * cm
            ])
        table.setStyle(TableStyle(styles))
        return table

    def create_signatures_table(self):
        """
        create table to manage
        signatures in of engineers 
        in first letter.
        """

        self.create_signature_name
        line = '_'*36
        first_engineer_full_name = f"""{self.engineer_one.first_name}
         {self.engineer_one.last_name}""".upper()  # space inbetween string

        if self.engineer_two.first_name:
            second_engineer_name = f"""{self.engineer_two.first_name}
             {self.engineer_two.last_name}""".upper()  # space inbetween string
            data = [
                [
                    self.create_signature_line(line),
                    self.create_signature_line(line)
                ],
                [
                    self.create_signature_name(first_engineer_full_name),
                    self.create_signature_name(second_engineer_name)
                ],
                [  # TODO verify linebreaks \t in certifications of each engineer
                    self.create_signature_line(
                        self.engineer_one.profile.certifications),
                    self.create_signature_line(
                        self.engineer_two.profile.certifications)
                ]
            ]
        else:
            data = [
                [self.create_signature_line(line), ''],
                [self.create_signature_name(first_engineer_full_name), ''],
                [self.create_signature_line(
                    self.engineer_one.profile.certifications),
                    '']
            ]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]
        table = Table(
            data,
            colWidths=[
                9 * cm,
                9 * cm],
            rowHeights=[
                0.4 * cm,
                0.5 * cm,
                0.5 * cm
            ])
        table.setStyle(TableStyle(styles))
        return table

    @staticmethod
    def _create_footer_table():
        """
        create table to manage
        elements in footer.
        """

        data = [[LINE_ONE], [LINE_TWO], [LINE_THREE]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]
        table = Table(
            data,
            colWidths=[
                18 * cm],
            rowHeights=[
                0.5 * cm,
                0.4 * cm,
                0.4 * cm
            ])
        table.setStyle(TableStyle(styles))
        return table

    @staticmethod
    def _create_analysis_table(analysis, recomendation):
        """
        create table of analysis
        of a measurement.
        """

        header_one = Paragraph(
            'ANÁLISIS DE VIBRACIÓN',
            style=STANDARD_CENTER)
        header_two = Paragraph(
            'CORRECTIVOS Y/O RECOMENDACIONES',
            style=STANDARD_CENTER)
        analysis = Paragraph(
            analysis,
            style=STANDARD)
        recomendation = Paragraph(
            recomendation,
            style=STANDARD)
        data = [
            [header_one],
            [analysis],
            [header_two],
            [recomendation]
        ]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]
        table = Table(
            data,
            colWidths=[18 * cm])
        table.setStyle(TableStyle(styles))
        return table

    @ staticmethod
    def graph_table(title, graph):
        """
        create a table containing
        an especified graphic.
        """

        title = Paragraph(title.upper(), style=STANDARD_CENTER)
        graph = Image(graph, width=17 * cm, height=6 * cm)
        data = [[title], [graph]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BACKGROUND', (0, 0), (0, 0), TABLE_BLUE),
            ('GRID', (0, 0), (-1, -1), 0.25, black)
        ]
        table = Table(data, colWidths=[18 * cm], rowHeights=[0.5 * cm, 7 * cm])
        table.setStyle(TableStyle(styles))
        return table

    def _header_one(self, canvas, doc):
        """
        method to be passed to PageTemplate
        objects on onPage keyword argument 
        to generate headers of measurements.
        """

        canvas.saveState()
        page = Paragraph(str(doc.page), style=BLACK_SMALL)
        w, h = page.wrap(self.width, 1 * cm)
        page.drawOn(canvas, self.leftMargin +
                    ((self.width - w) / 2), (29 * cm) - h)
        table = self._create_header_table()
        _, ht = table.wrap(self.width, 3 * cm)
        table.drawOn(canvas, self.leftMargin, 28 * cm - ht)
        canvas.restoreState()

    def _header_two(self, canvas, doc):
        """
        method to be passed to PageTemplate
        objects on onPage keyword argument 
        to generate basic headers.
        """

        canvas.saveState()
        page = Paragraph(str(doc.page), style=BLACK_SMALL)
        w, h = page.wrap(self.width, 1 * cm)
        page.drawOn(canvas, self.leftMargin +
                    ((self.width - w) / 2), (29 * cm) - h)
        canvas.restoreState()

    def _footer(self, canvas, doc):
        """
        method to be passed to PageTemplate
        objects on onPageEnd keyword argument
        to generate footers.
        """

        canvas.saveState()
        table = self._create_footer_table()
        _, h = table.wrap(self.width, self.bottomMargin)
        table.drawOn(canvas, self.leftMargin, (2 * cm - h) / 2)
        canvas.restoreState()

    def create_letter_header(self):
        """"
        create header containing engineer
        name and introduction line of date.
        """

        name = f'{self.user.first_name} {self.user.last_name}'
        date = Paragraph(
            f'Medellín, {CURRENT_DAY} de {MONTHS[CURRENT_MONTH - 1]} de {CURRENT_YEAR},',
            style=STANDARD)
        engineer_client = Paragraph(
            f"""Ingeniero:<br/><font name="Arial-Bold">{name.upper()}
            </font><br/>Dpto. de Mantenimiento <br/>Email: 
            <font color='blue'><a href={f'mailto:{self.user.email}'}>{self.user.email}</a></font>""",
            style=STANDARD)
        flowables = [
            date,
            Spacer(self.width, 1 * cm),
            engineer_client
        ]
        return flowables

    @staticmethod
    def create_letter_two_table():
        """
        create a table containing
        an especified graphic.
        """
        
        title_one = Paragraph('Rango de Velocidad efectiva RMS (mm/seg.)', style=BLACK_BOLD_CENTER)
        title_two = Paragraph('Tipos de Máquinas', style=BLACK_BOLD_CENTER)
        data = [
            [title_one, '', title_two,'', '', ''], 
            ['', '', 'Clase l', 'Clase ll', 'Clase lll', 'Clase lV'],
            ['', '', '', '', '', ''],
            ['28', '', 'D', 'D', 'D', 'D'],
            ['18', '', '', '', '', 'C'],
            ['11.2', '', '', '', 'C', ''],
            ['7.1', '', '', 'C', '', 'B'],
            ['4.5', '', 'C', '', 'B', ''],
            ['2.8', '', '', 'B', '', 'A'],
            ['1.8', '', 'B', '', 'A', ''],
            ['1.12', '', '', 'A', '', ''],
            ['0.71', '', 'A', '', '', ''],
            ['0.45', '', '', '', '', ''],
            ['0.28', '', '', '', '', ''],
            ]
        styles = [
            ('SPAN', (0, 0), (1, 2)),
            ('SPAN', (2, 0), (5, 0)),
            ('SPAN', (2, 1), (2, 2)),
            ('SPAN', (3, 1), (3, 2)),
            ('SPAN', (4, 1), (4, 2)),
            ('SPAN', (5, 1), (5, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (0, 4), (1, 4)),
            ('SPAN', (0, 5), (1, 5)),
            ('SPAN', (0, 6), (1, 6)),
            ('SPAN', (0, 7), (1, 7)),
            ('SPAN', (0, 8), (1, 8)),
            ('SPAN', (0, 9), (1, 9)),
            ('SPAN', (0, 10), (1, 10)),
            ('SPAN', (0, 11), (1, 11)),
            ('SPAN', (0, 12), (1, 12)),
            ('SPAN', (0, 13), (1, 13)),
            ('SPAN', (2, 3), (2, 6)),     
            ('SPAN', (2, 7), (2, 8)),
            ('SPAN', (2, 9), (2, 10)),
            ('SPAN', (2, 11), (2, 13)),
            ('SPAN', (3, 3), (3, 5)),
            ('SPAN', (3, 6), (3, 7)),
            ('SPAN', (3, 8), (3, 9)),
            ('SPAN', (3, 10), (3, 13)),
            ('SPAN', (4, 3), (4, 4)),
            ('SPAN', (4, 5), (4, 6)),
            ('SPAN', (4, 7), (4, 8)),
            ('SPAN', (4, 9), (4, 13)),
            ('SPAN', (5, 3), (5, 3)),
            ('SPAN', (5, 4), (5, 5)),
            ('SPAN', (5, 6), (5, 7)),
            ('SPAN', (5, 8), (5, 13)),
            #RED BACKGROUND
            ('BACKGROUND', (2, 3), (2, 6), Color(red=1, green=0, blue=0)),
            ('BACKGROUND', (3, 3), (3, 5), Color(red=1, green=0, blue=0)),
            ('BACKGROUND', (4, 3), (4, 4), Color(red=1, green=0, blue=0)),
            ('BACKGROUND', (5, 3), (5, 3), Color(red=1, green=0, blue=0)),
            #YELLOW BACKGROUND
            ('BACKGROUND', (2, 7), (2, 8), Color(red=1, green=1, blue=0)),
            ('BACKGROUND', (3, 6), (3, 7), Color(red=1, green=1, blue=0)),
            ('BACKGROUND', (4, 5), (4, 6), Color(red=1, green=1, blue=0)),
            ('BACKGROUND', (5, 4), (5, 5), Color(red=1, green=1, blue=0)),
            #GREEN ONE BACKGROUND
            ('BACKGROUND', (2, 9), (2, 10), Color(red=0, green=1, blue=0)),
            ('BACKGROUND', (3, 8), (3, 9), Color(red=0, green=1, blue=0)),
            ('BACKGROUND', (4, 7), (4, 8), Color(red=0, green=1, blue=0)),
            ('BACKGROUND', (5, 6), (5, 7), Color(red=0, green=1, blue=0)),
            #GREEN TWO BACKGROUND
            ('BACKGROUND', (2, 11), (2, 13), Color(red=(153/255), green=1, blue=(153/255))),
            ('BACKGROUND', (3, 10), (3, 13), Color(red=(153/255), green=1, blue=(153/255))),
            ('BACKGROUND', (4, 9), (4, 13), Color(red=(153/255), green=1, blue=(153/255))),
            ('BACKGROUND', (5, 8), (5, 13), Color(red=(153/255), green=1, blue=(153/255))),
            # FONT GRID AND ALIGNMENT
            ('FONTNAME', (0,3), (0, 13), 'Arial'),
            ('FONTNAME', (0,0), (5, 2), 'Arial-Bold'),
            ('FONTNAME', (2,3), (-1, -1), 'Arial-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.25, black),
            ('BOX', (0, 0), (-1, -1), 2, black),
            ('BOX', (0, 0), (-1, -1), 1, Color(red=0, green=0, blue=0)),
        ]
        table = Table(
            data, 
            colWidths=[2 * cm for _ in range(6)], 
            rowHeights=[0.5 * cm for _ in range(14)]
            )
        table.setStyle(TableStyle(styles))
        return table


    @staticmethod
    def create_table_title():
        """
        create a paragraph flowable to
        be used as a title for the tables.
        """

        title = Paragraph(
            'LECTURAS REGISTRADAS (@ptitude - SKF)', style=STANDARD_CENTER)
        return title

    @staticmethod
    def create_tendendy_title():
        """
        create a paragraph flowable to
        be used as a title for the 
        tendency graphs. 
        """

        title = Paragraph('GRAFICAS TENDENCIAS (En el tiempo)',
                          style=STANDARD_CENTER)
        return title

    @staticmethod
    def create_espectra_title():
        """
        create a paragraph flowable to
        be used as a title for the 
        tendency graphs. 
        """

        title = Paragraph('GRAFICAS ESPECTROS',
                          style=STANDARD_CENTER)
        return title

    @staticmethod
    def create_time_signal_title():
        """
        create a paragraph flowable to
        be used as a title for the 
        tendency graphs. 
        """

        title = Paragraph('GRAFICAS SEÑAL EN EL TIEMPO',
                          style=STANDARD_CENTER)
        return title

    @staticmethod
    def create_signature_line(string):
        return Paragraph(string, style=STANDARD)

    @staticmethod
    def create_signature_name(string):
        return Paragraph(string, style=BLACK_BOLD)

    @staticmethod
    def pictures_table(diagram_img, machine_img):
        """
        create a table containing the 
        diagram image and the machine image.
        """

        img_width = 7 * cm
        img_height = 6 * cm
        diagram_img = Image(
            diagram_img,
            width=img_width,
            height=img_height)
        machine_img = Image(
            machine_img,
            width=img_width,
            height=img_height)
        diagram = Paragraph('DIAGRAMA ESQUEMATICO', style=STANDARD)
        machine = Paragraph('IMAGEN MAQUINA', style=STANDARD)
        data = [[diagram, machine], [diagram_img, machine_img]]
        styles = [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.25, black),
            ('BACKGROUND', (0, 0), (1, 0), TABLE_BLUE)
        ]
        table = Table(
            data,
            colWidths=[
                9 * cm,
                9 * cm],
            rowHeights=[
                0.5 * cm,
                6 * cm
            ])
        table.setStyle(TableStyle(styles))
        return table

    # TODO finish these methods

    def machine_specifications_table(self):
        """
        create table detailing especifications 
        of each machine and their current severity.
        """

        data = None
        styles = None
        table = Table(data, colWidths=[18 * cm], rowHeights=[0.5 * cm, 7 * cm])
        table.setStyle(TableStyle(styles))
        return table