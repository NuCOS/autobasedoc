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


class Test_AutoBaseDoc(unittest.TestCase):
    """
    test class for reading in of the test case catalogue for ldm
    """

    @classmethod
    def setUpClass(cls):
        """
        do all necessary calculations that are the basis for the actual test
        """

        cls.textsize = 12

        cls.outname = os.path.realpath(
            os.path.join(__examples__, "MinimalExample.pdf"))

        # Begin of Documentation to Potable Document
        cls.doc = ar.AutoDocTemplate(
            cls.outname,
            onFirstPage=ar.drawFirstPage,
            onLaterPages=ar.drawLaterPage,
            onLaterSPages=ar.drawLaterLPage)

        cls.styles = ar.Styles()
        cls.styles.registerStyles()

        cls.contents = []

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        self.contents = []
        #doc.multiBuild(story)

        # If you want to append special behaviour of some Paragraph styles:
        self.styles.normal_left = ar.ParagraphStyle(
            name='normal', fontSize=6, leading=7, alignment=ar.TA_LEFT)

        # add title
        para = ar.Paragraph(u"Minimal Example Title", self.styles.title)
        self.contents.append(para)
        self.contents.append(ar.PageBreak())

        # Create an instance of TableOfContents. Override the level styles (optional)
        # and add the object to the story
        toc = ar.doTabelOfContents()
        self.contents.append(ar.Paragraph(u"Inhaltsverzeichnis", self.styles.h1))
        self.contents.append(toc)

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        pass

    def test_addTitle(self, inTemplate='LaterL', outTemplate='LaterL'):
        """
        # add title
        """
        ar.PageNext(self.contents, nextTemplate=inTemplate)
        self.contents.append(ar.PageBreak())
        para = ar.Paragraph(u"Minimal Example Title", self.styles.title)
        self.contents.append(para)
        ar.PageNext(self.contents, nextTemplate=outTemplate)
        self.contents.append(ar.PageBreak())

    def test_addChapter(self, nextTemplate='LaterL'):
        """
        # add chapter
        """
        ar.PageNext(self.contents, nextTemplate=nextTemplate)
        # Begin of First Chapter
        self.contents.append(ar.PageBreak())
        part = ar.doHeading("Text", self.styles.h1)
        for p in part:
            self.contents.append(p)

    def test_addSubChapter(self):
        """
        # add subchapter
        """
        part = ar.doHeading(testVal1["subch"], self.styles.h2)
        for p in part:
            self.contents.append(p)

    def test_addParagraph(self):
        """
        # add paragraph
        """
        para = ar.Paragraph(
            u"""My Text that I can write here
            or take it from somewhere like shown in the next paragraph.""",
            self.styles.normal)
        self.contents.append(para)

    def test_addFigure(self, title=u"my first data"):
        """
        # add figure
        """
        para = ar.Paragraph(u"Fig. " + str(self.doc.figcounter()) + title,
                            self.styles.caption)
        self.contents.append(para)

    def test_addTable(self, title=u"Table is here."):
        """
        # add figure
        """
        para = ar.Paragraph(u"Fig. " + str(self.doc.figcounter()) + title,
                            self.styles.caption)
        self.contents.append(para)
        self.contents.append(ar.Paragraph("Table is here.",
                                          self.styles.normal))

    def test_buildDoc(self):
        """
        last test
        """
        self.doc.multiBuild(self.contents)


if __name__ == "__main__":

    unittest.main()
