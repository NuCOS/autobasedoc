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

from autobasedoc import ar
from autobasedoc import ap
from autobasedoc import _baseFontNames

from autobasedoc.autorpt import addPlugin

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


def drawFirstPage(canv, doc):
    """
    This is the Title Page Template (Portrait Oriented)
    """
    canv.saveState()
    #set Page Size
    frame, pagesize = doc.getFrame('FirstP', orientation="Portrait")

    canv.setPageSize(pagesize)
    canv.setFont(_baseFontNames["normal"], doc.fontSize)

    doc.centerM = (frame._width -
                   (frame._leftPadding + frame._rightPadding)) / 2
    doc.leftM = frame._leftPadding
    doc.rightM = frame._width - frame._rightPadding
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

    doc.centerM = (frame._width -
                   (frame._leftPadding + frame._rightPadding)) / 2
    doc.leftM = frame._leftPadding
    doc.rightM = frame._width - frame._rightPadding
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

    doc.centerM = (frame._width -
                   (frame._leftPadding + frame._rightPadding)) / 2
    doc.leftM = frame._leftPadding
    doc.rightM = frame._width - frame._rightPadding
    doc.headM = (frame._height - frame._topPadding) + doc.topM
    doc.bottomM = frame._bottomPadding - doc.topM

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()


class Test_AutoBaseDoc(unittest.TestCase):
    """
    test class for writing pdf file with PdfImage from::

        from autobasedoc import ap

    """

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
                self.addLegendWithFigure()
                self.addParagraph()
                self.addSubChapter()
                self.addParagraph()
                self.addTable()
                self.addParagraph()
                self.addLegendWithFigure()

    #@unittest.skip("simple test")
    def test_buildSimple(self, testTemplate='LaterP'):
        """
        test run figure simple

        switch template on figure
        """

        testTemplate = ['LaterP', 'LaterL']

        for templt in testTemplate:
            with self.subTest(templt=templt):
                self.addFigure()

    def test_buildLegendWithFigure(self, testTemplate='LaterP'):
        """
        test run figure simple

        switch template on figure
        """

        testTemplate = ['LaterP', 'LaterL']

        for templt in testTemplate:
            with self.subTest(templt=templt):
                self.addLegendWithFigure()

    #@unittest.skip("add title")
    def addTitle(self, para=u"Minimal Example Title", outTemplate='LaterL'):
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
    def addChapter(self, para="Text", nextTemplate='LaterL', sty=None):
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
    def addParagraph(self,
                     para=u"""My Text that I can write here
            or take it from somewhere like shown in the next paragraph.""",
                     sty=None):
        """
        # add paragraph
        """
        if sty is None:
            sty = self.styles.normal
        para = ar.Paragraph(para, sty)
        self.contents.append(para)
        
    def addFigure(self):
        """
        # add SIMPLE figure
        """

        img = self.simpleFigure()
        
        self.contents.append(img)

    #@unittest.skip("add figure")
    def addLegendWithFigure(self,
                  para=u"""My Text that I can write here
            or take it from somewhere like shown in the next paragraph.""",
                  titlename=u"my first plot with autobasedoc",
                  sty=None):
        """
        # add figure
        """
        para = ar.Paragraph(u"Fig. " + str(self.doc.figcounter()) + para,
                            self.styles.caption)

        self.contents.append(para)

        if sty is None:
            sty = self.styles

        img, leg = self.plotFigure()
        self.contents.append(leg)
        self.contents.append(img)

        #ar.doImage(img, self.doc, titlename, sty)

    @ap.autoPdfImg
    def simpleFigure(canvaswidth=5):#[inch]
        fig, ax = ap.plt.subplots() #figsize=(canvaswidth,canvaswidth)
        fig.suptitle("My Plot",fontproperties=fontprop)
        x=[1,2,3,4,5,6,7,8]
        y=[1,6,8,3,9,3,4,2]
        ax.plot(x,y,label="legendlabel")
        
        ax.legend(mode=None,
               borderaxespad=0.,
               loc='center',        # the location of the legend handles
               handleheight=None,   # the height of the legend handles
               #fontsize=9,         # prop beats fontsize
               markerscale=None,
               prop=fontprop,
               fancybox=True,
               )
        
        return fig

    @ap.autoPdfImage
    def plotFigure(canvaswidth=5):  #[inch]

        fig, ax = ap.plt.subplots() #figsize=(canvaswidth, canvaswidth)
        fig.suptitle("My Plot", fontproperties=fontprop)
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        y = [1, 6, 8, 3, 9, 3, 4, 2]
        ax.plot(x, y, label="legendlabel")
        nrow, ncol = 1, 1
        handels, labels = ax.get_legend_handles_labels()

        leg_fig = ap.plt.figure() #figsize=(canvaswidth, 0.2 * nrow)

        leg = leg_fig.legend(
            handels,
            labels,  #labels = tuple(bar_names)
            ncol=ncol,
            mode=None,
            borderaxespad=0.,
            loc='center',  # the location of the legend handles
            handleheight=None,  # the height of the legend handles
            #fontsize=9,         # prop beats fontsize
            markerscale=None,
            frameon=False,
            prop=fontprop
            #fancybox=True,
        )

        return fig, leg_fig, leg

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
