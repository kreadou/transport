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

class ImprimerDoc1():
    def __init__(self):
        self.temps=''
        self.story=[]
        self.largCol=160 #en portrait
        self.positionPage=7 #en portrait
        self.pageInfo=''
        self.logo = ""
        self.enteteSurToutePage=False
        self.entete=[['','',''],['','',''],['','',''],['','',''], ['','',''], ['','',''], ['','','']]
        ts = TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                         ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
                         ('ALIGN', (1,1), (1,1), 'CENTER')])
        
        self.t=Table(self.entete,[160,160,160],len(self.entete)*[0.5*cm])
        self.t.setStyle(ts)
        self.tSauve=self.t
        #self.t.hAlign=0
        
        self.t1=Table(self.entete,[226,226,226],len(self.entete)*[0.5*cm])
        self.t1.setStyle(ts)
        #self.t1.hAlign=0
        
    def myFirstPage(self, canvas, doc):
        canvas.saveState()
        #self.story.insert(0,Paragraph('', self.styles["Title"]))
        #self.story.insert(0,Paragraph('', self.styles["Title"]))
        self.story.insert(0,self.t)
        #canvas.setFont('Times-Roman',9)
        #canvas.setLineWidth(0.5)
        #canvas.line(200,760,400,760)
        canvas.restoreState()

    def myLaterPages(self, canvas, doc):
        canvas.saveState()
        if self.enteteSurToutePage:self.story.insert(0,self.t)
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
    
    def miseAjourEntete(self, canvas, doc):
        pass
    
    def go(self, fichier='fichier.pdf', format=A4, topMargin=20):#┌
        try:
            self.doc = SimpleDocTemplate(fichier,pagesize=format, rightMargin=72,leftMargin=72,topMargin=20,bottomMargin=18)
            self.doc.build(self.story, onFirstPage=self.myFirstPage, onLaterPages=self.myLaterPages)
        except:pass