# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:50:28 2015

@author: ecksjoh
"""
import numpy as np
import sys
import os

__root__ = os.path.dirname(__file__)

folder = "../"

importpath=os.path.realpath(os.path.join(__root__,folder))

#print(importpath)
sys.path.append(importpath)

from autoreport import autoreport as ar 

ap=ar.ap

ar._baseFontName,ar._baseFontNameB,ar._baseFontNameI,ar._baseFontNameBI = ar.setFonts(typ='sans-serif')

fpath = os.path.join(ap.__font_dir__,'calibri.ttf')
font = ap.ft2font.FT2Font(fpath)
ap.fontprop = ap.ttfFontProperty(font)

fontprop = ap.fm.FontProperties(family='sans-serif',
                                #name=ap.fontprop.name,
                                fname=ap.fontprop.fname,
                                size=None,
                                stretch=ap.fontprop.stretch,
                                style=ap.fontprop.style,
                                variant=ap.fontprop.variant,
                                weight=ap.fontprop.weight)

name_loc = "."#"../data"
__examples__ = os.path.realpath(os.path.join(__root__,name_loc))

if __name__ == "__main__":
    # create some Data first
    textsize = 12

    Content = {}
    Context = {}
    Chapters = [u"Kapitel 1",]
    Subchapters = [u"Unterkapitel 1", u"Unterkapitel 2"]

    mu, sigma = 100, 15
    #x = mu + sigma*np.random.randn(10000)
    x = np.random.uniform(1, 6, size=150)

    Content.update({"my first data":x})
    Context.update({"my first data":"What I always wanted to say about data that has some data title"})

    # Begin of Documentation to Potable Document
    outname = os.path.realpath(os.path.join(__examples__,"MinimalExample.pdf"))
    doc = ar.AutoDocTemplate(outname,
                             onFirstPage=ar.drawFirstPage,
                             onLaterPages=ar.drawLaterPage,
                             onLaterSPages=ar.drawLaterLPage)

    contents = []
    #doc.multiBuild(story)
    styles=ar.Styles()
    styles.registerStyles()

    # If you want to append special behaviour of some Paragraph styles:
    styles.normal_left = ar.ParagraphStyle(name='normal', 
                                              fontSize=6, 
                                              leading = 7, 
                                              alignment=ar.TA_LEFT)

    # add title
    para = ar.Paragraph(u"Minimal Example Title", styles.title)
    contents.append(para)
    contents.append(ar.PageBreak())

    # Create an instance of TableOfContents. Override the level styles (optional)
    # and add the object to the story
    toc = ar.doTabelOfContents()
    contents.append(ar.Paragraph(u"Inhaltsverzeichnis", styles.h1))
    contents.append(toc)
    contents.append(ar.PageBreak())

    # Begin of First Chapter
    part = ar.doHeading("Text", styles.h1)
    for p in part:
        contents.append(p)

    para = ar.Paragraph(u"My Text that I can write here or take it from somewhere like shown in the next paragraph.", styles.normal)
    contents.append(para)

    part = ar.doHeading(Subchapters[1], styles.h2)
    for p in part:
        contents.append(p)

    title = u"my first data"

    #para = ar.doTableAsParagraph('text',ar.styles.p3,doc.width,outlineText="outline to text")
    #contents.append(para)

    para = ar.Paragraph(Context[title], styles.normal)
    contents.append(para)


    para = ar.Paragraph(u"Fig. " + str(doc.figcounter()) + title,styles.caption)
    contents.append(para)

    contents.append(ar.Paragraph("Table is here.",styles.normal))
#    contents.append(ar.NextPageTemplate('LaterL'))
#    contents.append(ar.PageBreak())

    ar.PageNext(contents,nextTemplate='LaterL')
    contents.append(ar.Paragraph("Pictures are to be placed here.",styles.normal))

    contents.append(ar.PageBreak())

    #write the buffer to the document
    #doc.build(contents)

    doc.multiBuild(contents)