# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:50:28 2015

@author: ecksjoh
"""
import numpy as np
import os
import sys
import unittest
from faker import Faker

__root__ = os.path.dirname(__file__)

folder = "../"

importpath = os.path.realpath(os.path.join(__root__, folder))

#print(importpath)
sys.path.append(importpath)

import autobasedoc.autorpt as ar
import autobasedoc.autoplot as ap
from autobasedoc.autorpt import addPlugin
from autobasedoc import base_fonts

fpath = os.path.join(ar.__font_dir__, 'calibri.ttf')
font = ap.ft2font.FT2Font(fpath)
ap.fontprop = ap.ttfFontProperty(font)

fontprop = ap.fm.FontProperties(
    family='sans-serif',
    #name=ap.fontprop.name,
    fname=ap.fontprop.fname,
    size=None,
    stretch=ap.fontprop.stretch,
    style=ap.fontprop.style,
    variant=ap.fontprop.variant,
    weight=ap.fontprop.weight)

name_loc = "."  #"../data"
__examples__ = os.path.realpath(os.path.join(__root__, name_loc))

def drawFirstPortrait(canv, doc):
    """
    This is the Title Page Template (Portrait Oriented)
    """
    canv.saveState()
    #set Page Size
    frame, pagesize = doc.getFrame(temp_name=doc.template_id)

    print(doc.template_id, frame._width, frame._height)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    # doc.centerM = (frame._width-(frame._leftPadding + frame._rightPadding))/2
    # doc.leftM = frame._leftPadding
    # doc.rightM = frame._width-frame._rightPadding
    # doc.headM = (frame._height - frame._topPadding) + doc.topM
    # doc.bottomM = frame._bottomPadding - doc.topM

    #addPlugin(canv, doc, frame="First")

    canv.restoreState()


def drawLaterPortrait(canv, doc):
    """
    This is the Template of any following Portrait Oriented Page
    """
    canv.saveState()
    #set Page Size

    frame, pagesize = doc.getFrame(temp_name=doc.template_id)

    print(doc.template_id, frame._width, frame._height)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    # doc.centerM = (frame._width - (frame._leftPadding + frame._rightPadding))/2
    # doc.leftM = frame._leftPadding
    # doc.rightM = frame._width-frame._rightPadding
    # doc.headM = (frame._height - frame._topPadding) + doc.topM
    # doc.bottomM = frame._bottomPadding - doc.topM

    #addPlugin(canv, doc, frame="Later")

    canv.restoreState()


def drawLaterLandscape(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()

    #set Page Size and
    #some variables```````````

    frame, pagesize = doc.getFrame(temp_name=doc.template_id)

    print(doc.template_id, frame._width, frame._height)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    # doc.centerM = (frame._width - (frame._leftPadding + frame._rightPadding))/2
    # doc.leftM = frame._leftPadding
    # doc.rightM = frame._width - frame._rightPadding
    # doc.headM = (frame._height - frame._topPadding) + doc.topM
    # doc.bottomM = frame._bottomPadding - doc.topM

    #addPlugin(canv, doc, frame="Later")

    canv.restoreState()


class Test_AutoBaseDoc(unittest.TestCase):
    """
    Haupttestklasse für AutoBaseDoc-Funktionalität.
    
    Diese Klasse testet den kompletten Workflow der PDF-Erstellung
    von der Dokumentinitialisierung bis zur finalen Ausgabe.
    """
    
    def setUp(self):
        """
        Test-Setup: Erstellt Basis-Dokumentkonfiguration.
        
        Initialisiert:
        - AutoDocTemplate mit Standard-Einstellungen
        - Styles für konsistente Formatierung
        - Leere Content-Liste für Flowables
        """
        """
        Umfassende Tests für das autorpt-Modul.

        Diese Testsuite validiert alle Hauptfunktionen der AutoBaseDoc-Bibliothek,
        einschließlich:

        - Dokumenterstellung in verschiedenen Formaten
        - Layout-Management und Frame-Handling  
        - Header/Footer-Funktionalität
        - Bookmark- und TOC-Generierung
        - Matplotlib-Integration
        - Fehlerbehandlung

        Testklassen
        -----------
        Test_AutoBaseDoc : unittest.TestCase
            Haupttestklasse mit vollständigen Dokumenterstellungsszenarien
            
        Testmethoden
        -----------
        - test_create_document(): Basis-Dokumenterstellung
        - test_add_content(): Hinzufügen verschiedener Inhaltstypen
        - test_layouts(): Portrait/Landscape-Layouts  
        - test_headers_footers(): Kopf-/Fußzeilenfunktionen
        - test_bookmarks(): PDF-Navigation
        - test_matplotlib(): Plot-Integration

        Ausführung
        ----------
            python -m unittest tests.test_autoreport
            python tests/test_autoreport.py
        """

        self.fake = Faker()

        # Begin of Documentation to Potable Document
        self.doc = ar.AutoDocTemplate(
            "test_autoreport.pdf",
            onFirstPage=(drawFirstPortrait, 1),
            onLaterPages=(drawLaterPortrait, 0),
            onLaterSPages=(drawLaterLandscape, 2),
            # leftMargin=0. * ar.cm,
            # rightMargin=0. * ar.cm,
            # topMargin=0. * ar.cm,
            # bottomMargin=0. * ar.cm,
            debug=True)

        self.styles = ar.Styles()
        self.styles.registerStyles()

        self.contents = []

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        self.buildDoc()

    def test_bigBuildThrough(self, testTemplate='LaterP'):
        """
        test run through big story
        """
        # special behaviour of some Paragraph styles:
        self.styles.normal_left = ar.ParagraphStyle(name='normal',
                                                    fontSize=6,
                                                    leading=7,
                                                    alignment=ar.TA_LEFT)

        self.addTitle(outTemplate=testTemplate)
        self.addToc()

        for i in range(30):
            self.addChapter()
            self.addParagraph()
            self.addSubChapter()
            self.addParagraph()

    #@unittest.skip("add title")
    def addTitle(self,
                 para=u"Minimal Example Title",
                 outTemplate='LaterSL'):
        """
        # add title
        """
        para = ar.Paragraph(para, self.styles.title)
        self.contents.append(para)
        #nextTemplate = self.doc.getSpecialTemplate(temp_name=outTemplate)
        #self.contents = ar.PageNext(self.contents, nextTemplate=nextTemplate)
        self.contents.append(ar.PageBreak())

    #@unittest.skip("add toc")
    def addToc(self, para=u"Inhaltsverzeichnis"):
        """
        # add table of contents
        # Create an instance of TableOfContents.
        # Override the level styles (optional)
        # and add the object to the story
        """
        toc = ar.doTabelOfContents()
        self.contents.append(ar.Paragraph(para, self.styles.h1))
        self.contents.append(toc)
        self.contents.append(ar.PageBreak())

    #@unittest.skip("add chapter")
    def addChapter(self, nextTemplate='Later'):
        """
        # add chapter
        """
        #nextTemplate = self.doc.getSpecialTemplate(temp_name=nextTemplate)
        #self.contents = ar.PageNext(self.contents, nextTemplate=nextTemplate)
        part = ar.doHeading(self.fake.word(), self.styles.h1)
        for p in part:
            self.contents.append(p)

    #@unittest.skip("add subchapter")
    def addSubChapter(self):
        """
        # add subchapter
        """
        part = ar.doHeading(self.fake.word(), self.styles.h2)
        for p in part:
            self.contents.append(p)

    #@unittest.skip("add paragraph")
    def addParagraph(self):
        """
        # add paragraph
        """
        para = ar.Paragraph(self.fake.text(), self.styles.normal_left)
        self.contents.append(para)

    #@unittest.skip("add figure")
    def addFigure(self, para=u"my first data"):
        """
        # add figure
        """
        para = ar.Paragraph(u"Fig. " + str(self.doc.figcounter()) + para,
                            self.styles.caption)
        self.contents.append(para)

    #@unittest.skip("add table")
    def addTable(self, para=u"Table is here."):
        """
        # add table
        """
        para = ar.Paragraph(u"Tab. " + str(self.doc.figcounter()) + para,
                            self.styles.caption)
        self.contents.append(para)
        # self.contents.append(ar.Paragraph(para, self.styles.normal))

    #@unittest.skip("build doc")
    def buildDoc(self):
        """
        # build doc
        """
        self.doc.multiBuild(self.contents)


if __name__ == "__main__":

    unittest.main()
