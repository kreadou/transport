# -*- coding:utf-8 -*-
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4,A3,A5,A6,letter, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
import time

styles = getSampleStyleSheet()

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]

class ImprimerDoc2C():
    def __init__(self):
        self.story=[]
        
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',8)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',8)
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
    
    def go(self, fichier='fichier.pdf', format=A4, topMargin=20):#┌
        try:
            self.doc = SimpleDocTemplate(fichier, pagesize=format, rightMargin=72,leftMargin=72,topMargin=15,bottomMargin=18)
            self.doc.build(self.story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
        except:pass    