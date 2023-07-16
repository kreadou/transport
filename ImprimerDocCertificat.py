# -*- coding:utf-8 -*-
from reportlab.lib.pagesizes import A4,A3,A5,A6,letter, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
""" modules reportLabs pour l'impression en pdf """
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
#from pyPdf import PdfFileWriter, PdfFileReader 

""" class pour imprimer en pdf """
from reportlab.lib.units import inch

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='JustifyInd', alignment=TA_JUSTIFY, firstLineIndent=24))
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

import os
from datetime import *
import time

class ImprimerDoc():
    def __init__(self):
        self.temps=''
        self.story=[]
        self.largCol=160 #en portrait
        self.positionPage=7 #en portrait
        self.enteteSurToutePage=False
        self.pageInfo=''
        self.pageInfo1=''
        self.pageInfo2=''
        self.piedPage1=''#"Abidjan - Cocody, route de l'Université, boulevard F. Mitterand face Ecole de Gendarmerie"
        self.piedPage2=''#"Tél.: 22 48 48 12 Fax (225) 22 48 48 14 CC:02 193 40 H RC: 279162 N° Compte standard : 0100101102800"
        self.piedPage3=''#"Centre impôts Cocody 17 BP 84 Abidjan 17 - wwww.hec.ci / e-mail : info@hec.ci"
        self.logo = ""
        self.entete=[['','','','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','','','','']]
        ts=TableStyle([#('GRID', (0,0), (-1,-1), 1, colors.black), 
        ('SIZE', (0,0), (-1,-1), 10),
        
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
        ('ALIGN', (0,0), (0,-3), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        
        ('SPAN', (3,2), (6,2)),
        ('ALIGN', (3,2), (6,2), 'CENTER'),
        ('SPAN', (3,3), (6,3)),
        ('ALIGN', (3,3), (6,3), 'CENTER'),
        ('FONTNAME', (3,3), (6,3), 'Times-BoldItalic'),
        
        #('SIZE', (3,0), (4,0), 8),
        ('ALIGN', (3,0), (4,0), 'CENTER'),
        ])
        
        self.t=Table(self.entete,[50],len(self.entete)*[0.4*cm])
        self.t.setStyle(ts)
        self.tSauve=self.t
        #self.t.hAlign=0
        
        self.entete2=[['','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','',''],
                     ['','','','','','','','','','','','','','']]
        td=TableStyle([#('GRID', (0,0), (-1,-1), 1, colors.black), 
        ('SIZE', (0,0), (-1,-1), 12),
        
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
        ('ALIGN', (0,0), (0,-3), 'LEFT'),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        
        ('SPAN', (3,2), (6,2)),
        ('ALIGN', (3,2), (6,2), 'CENTER'),
        ('SPAN', (3,3), (6,3)),
        ('ALIGN', (3,3), (6,3), 'CENTER'),
        ('FONTNAME', (3,3), (6,3), 'Times-BoldItalic'),
        
        #('SIZE', (3,0), (4,0), 8),
        ('ALIGN', (3,0), (4,0), 'CENTER'),
        ])
        
        self.t1=Table(self.entete2,[56],len(self.entete)*[0.4*cm])
        self.t1.setStyle(td)
        #self.t1.hAlign=0
        
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        #self.story.insert(0,Paragraph('', self.styles["Title"]))
        #self.story.insert(0,Paragraph('', self.styles["Title"]))
        self.story.insert(0,self.t)
        #canvas.setFont('Times-Roman',9)
        #canvas.setLineWidth(0.5)
        #canvas.line(200,760,400,760)
        canvas.setFont('Times-Roman',9)
        self.temps = str(time.strftime('%d/%m/%y à %H:%M',time.localtime()))
        canvas.drawString((self.positionPage-1)*inch, 0.3*inch, "le %s - Page %s" % (self.temps, self.doc.page))
        canvas.drawString(inch, 0.3*inch, "%s" % self.pageInfo)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString((self.positionPage-1)*inch, 0.3*inch, "le %s - Page %s" %(self.temps, self.doc.page))
        canvas.drawString(inch, 0.3*inch, "%s" % self.pageInfo)
        canvas.restoreState()
        
   
        
    def header(self, txt, style=styles["Heading1"], klass=Paragraph, sep=0.3):
        s = Spacer(0.2*inch, sep*inch)
        self.story.append(s)
        para = klass(txt, style)
        self.story.append(para)
    
    def p(self, txt):
        return self.header(txt, style=self.ParaStyle, sep=0.1)

    def pre(self, txt):
        s = Spacer(0.1*inch, 0.1*inch)
        self.story.append(s)
        p = Preformatted(txt, self.PreStyle)
        self.story.append(p)
    
    def miseAjourEntete(self, canvas, doc):
        pass
    
    def go(self, fichier='fichier.pdf', format=A4, topMargin=20):#┌
        try:
            self.doc = SimpleDocTemplate(fichier,pagesize=format, rightMargin=24,leftMargin=24,topMargin=15,bottomMargin=18)
            self.doc.build(self.story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
        except:pass    