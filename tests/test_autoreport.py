# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:50:28 2015

@author: ecksjoh
"""
import numpy as np
import os
import sys
import unittest

__root__ = os.path.dirname(__file__)

folder = "../"

importpath = os.path.realpath(os.path.join(__root__, folder))

#print(importpath)
sys.path.append(importpath)

import autobasedoc.autorpt as ar
import autobasedoc.autoplot as ap
from autobasedoc.autorpt import addPlugin
from autobasedoc import _baseFontNames

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

# create some Data first

testVal1 = dict(
    ch="Kapitel",
    subch="Unterkapitel",
    para="What I always wanted to say about data that has some data title",
    mu=100,
    sigma=15)

testVal2 = dict(
    ch="Test Values",
    subch="Test Case",
    para="What I always wanted to say about data that has some data title",
    mu=80,
    sigma=23)

testMeta = dict(
    chapter1=dict(
        para1=f"""{testVal1["para"]}
        {testVal2["para"]}
        {testVal1["para"]}
        {testVal2["para"]}""",
        subchapter=testVal1["ch"],
        displayName=f"%s 1" % testVal1["ch"],
        x=np.random.uniform(1, 6, size=150),
        y=testVal1["mu"] + testVal1["sigma"] * np.random.randn(10000),
        items=[u"Unterkapitel 1", u"Unterkapitel 2"]),
    chapter2=dict(
        para1=f"""{testVal1["para"]}
        {testVal2["para"]}
        {testVal1["para"]}
        {testVal2["para"]}""",
        subchapter=testVal2["ch"],
        displayName=f"%s 2" % testVal2["ch"],
        x=testVal1["mu"] + testVal1["sigma"] * np.random.randn(10000),
        y=testVal2["mu"] + testVal2["sigma"] * np.random.randn(10000),
        items=[u"Unterkapitel 1", u"Unterkapitel 2"]))

tcDict = {}
# {value: testVal1.get(value) for value in testMeta.values()}


def drawFirstPage(canv, doc):
    """
    This is the Title Page Template (Portrait Oriented)
    """
    canv.saveState()
    #set Page Size
    frame, pagesize = doc.getFrame('FirstP', orientation="Portrait")

    canv.setPageSize(pagesize)
    canv.setFont(_baseFontNames["normal"], doc.fontSize)

    doc.centerM = (frame._width-(frame._leftPadding + frame._rightPadding))/2
    doc.leftM = frame._leftPadding
    doc.rightM = frame._width-frame._rightPadding
    doc.headM = (frame._height - frame._topPadding) + doc.topM
    doc.bottomM = frame._bottomPadding - doc.topM

    addPlugin(canv, doc, frame="First")

    canv.restoreState()


def drawLaterPage(canv, doc):
    """
    This is the Template of any following Portrait Oriented Page
    """
    canv.saveState()
    #set Page Size

    frame, pagesize = doc.getFrame('LaterP', orientation="Portrait")

    canv.setPageSize(pagesize)
    canv.setFont(_baseFontNames["normal"], doc.fontSize)

    doc.centerM = (frame._width - (frame._leftPadding + frame._rightPadding))/2
    doc.leftM = frame._leftPadding
    doc.rightM = frame._width-frame._rightPadding
    doc.headM = (frame._height - frame._topPadding) + doc.topM
    doc.bottomM = frame._bottomPadding - doc.topM

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()


def drawLaterLPage(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()

    #set Page Size and
    #some variables

    frame, pagesize = doc.getFrame('LaterL', orientation="Landscape")

    canv.setPageSize(pagesize)
    canv.setFont(_baseFontNames["normal"], doc.fontSize)

    doc.centerM = (frame._width - (frame._leftPadding + frame._rightPadding))/2
    doc.leftM = frame._leftPadding
    doc.rightM = frame._width - frame._rightPadding
    doc.headM = (frame._height - frame._topPadding) + doc.topM
    doc.bottomM = frame._bottomPadding - doc.topM

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()


class Test_AutoBaseDoc(unittest.TestCase):
    """
    test class for writing pdf file with AutoDocTemplate and Styles

    If you want to append special behaviour of some Paragraph styles::

        self.styles.normal_left = ar.ParagraphStyle(
            name='normal', fontSize=6, leading=7, alignment=ar.TA_LEFT)

    performance test on add and multi build
    This shows we dont have linear cost increase:

    # 10 in 0.67 seconds; per ch_pair:= 0,067
    # 100 in 2.964 seconds; per ch_pair:= 0,029
    # 200 in 7.801 seconds; per ch_pair:= 0,039
    # 400 in 27.064 seconds; per ch_pair:= 0,06016
    # 500 in 44.385 seconds; per ch_pair:= 0,0887
    # 600 in 63.645 seconds; per ch_pair:= 0,1
    # 800 in 120.183 seconds; per ch_pair:= 0,15
    # 1000 in 200.063 seconds; per ch_pair:= 0,2
    """

    @classmethod
    def setUpClass(cls):
        """
        do all necessary calculations that are the basis for the actual test
        """

        cls.textsize = 12

        cls.outname = os.path.realpath(
            os.path.join(__examples__, "MinimalExample.pdf"))
        cls.doc = None
        cls.contents = []
        cls.styles = None

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.

        Has to be run to set up the test
        """
        # Begin of Documentation to Potable Document
        self.doc = ar.AutoDocTemplate(
            self.outname,
            onFirstPage=drawFirstPage,
            onLaterPages=drawLaterPage,
            onLaterSPages=drawLaterLPage)

        self.styles = ar.Styles()
        self.styles.registerStyles()

        self.contents = []

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        self.buildDoc()

    #@unittest.skip("simple test")
    def test_buildThrough(self, testTemplate='LaterP'):
        """
        test run through story

        switch template on chapters
        """
        # special behaviour of some Paragraph styles:
        self.styles.normal_left = ar.ParagraphStyle(
            name='normal', fontSize=6, leading=7, alignment=ar.TA_LEFT)

        self.addTitle(outTemplate=testTemplate)
        self.addToc()

        testTemplate = ['LaterP', 'LaterL']

        for templt in testTemplate:
            with self.subTest(templt=templt):
                self.addChapter(nextTemplate=templt)
                self.addParagraph()
                self.addSubChapter()
                self.addParagraph()
                self.addSubChapter()
                self.addParagraph()
                self.addTable()
                self.addParagraph()
                self.addFigure()

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

        testData = [
            # ch, ch_para, sub_ch, sub_ch_para
            (testVal1['ch'], testVal1['para'], testVal1['subch'],
             testVal1['para']),
            (testVal2['ch'], testVal2['para'], testVal2['subch'],
             testVal1['para']),
        ] * 20

        for ch, ch_para, sub_ch, sub_ch_para in testData:
            with self.subTest(ch=ch,
                              ch_para=ch_para,
                              sub_ch=sub_ch,
                              sub_ch_para=sub_ch_para):

                self.addChapter(nextTemplate=testTemplate,
                                para=ch,
                                sty=self.styles.normal_left)
                self.addParagraph(para=ch_para)
                self.addSubChapter(para=sub_ch)
                self.addParagraph(para=sub_ch_para)

    #@unittest.skip("add title")
    def addTitle(self,
                 para=u"Minimal Example Title",
                 outTemplate='LaterL'):
        """
        # add title
        """
        para = ar.Paragraph(para, self.styles.title)
        self.contents.append(para)
        ar.PageNext(self.contents, nextTemplate=outTemplate)
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

    #@unittest.skip("add chapter")
    def addChapter(self,
                   para="Text",
                   nextTemplate='LaterL',
                   sty=None):
        """
        # add chapter
        """
        # default style h1
        if sty is None:
            sty = self.styles.h1
        ar.PageNext(self.contents, nextTemplate=nextTemplate)
        # Begin of First Chapter
        self.contents.append(ar.PageBreak())
        part = ar.doHeading(para, sty)
        for p in part:
            self.contents.append(p)

    #@unittest.skip("add subchapter")
    def addSubChapter(self, para=testVal1["subch"]):
        """
        # add subchapter
        """
        part = ar.doHeading(para, self.styles.h2)
        for p in part:
            self.contents.append(p)

    #@unittest.skip("add paragraph")
    def addParagraph(self, para=u"""My Text that I can write here
            or take it from somewhere like shown in the next paragraph.""",
            sty=None):
        """
        # add paragraph
        """
        if sty is None:
            sty = self.styles.normal
        para = ar.Paragraph(para, sty)
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
        para = ar.Paragraph(u"Fig. " + str(self.doc.figcounter()) + para,
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
