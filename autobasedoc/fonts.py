"""
fonts
=====

.. module:: fonts
   :platform: Unix, Windows
   :synopsis: font utils

.. moduleauthor:: Johannes Eckstein

"""

import os

from autobasedoc import base_fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import getFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping


def registerFont(faceName, afm, pfb):
    """
    Helvetica BUT AS AFM

    The below section is NOT equal to::

        _baseFontName  ='Helvetica'
        _baseFontNameB ='Helvetica-Bold'
        _baseFontNameI ='Helvetica-Oblique'
        _baseFontNameBI='Helvetica-BoldOblique'

    we will mapp afm files from matplotlib with pfb files from reportlab

    this will give embedded Type1 Face Fonts

    """
    afm = os.path.join(__font_dir__, "".join(afm, ".afm"))
    pfb = os.path.join(__font_dir__, "".join(pfb, ".pfb"))

    face = pdfmetrics.EmbeddedType1Face(afm, pfb)
    pdfmetrics.registerTypeFace(face)
    font = pdfmetrics.Font(faceName, faceName, 'WinAnsiEncoding')
    pdfmetrics.registerFont(font)


def setTtfFonts(familyName,
                font_dir,
                normal=(None, None),
                bold=(None, None),
                italic=(None, None),
                bold_italic=(None, None)):
    """
    Sets fonts for True Type Fonts
    """
    normalName, normalFile = normal
    boldName, boldFile = bold
    italicName, italicFile = italic
    bold_italicName, bold_italicFile = bold_italic

    pdfmetrics.registerFont(
        TTFont(normalName, os.path.join(font_dir, normalFile)))
    pdfmetrics.registerFont(TTFont(boldName, os.path.join(font_dir, boldFile)))
    pdfmetrics.registerFont(
        TTFont(italicName, os.path.join(font_dir, italicFile)))
    pdfmetrics.registerFont(
        TTFont(bold_italicName, os.path.join(font_dir, bold_italicFile)))

    addMapping(familyName, 0, 0, normalName)
    addMapping(familyName, 1, 0, boldName)
    addMapping(familyName, 0, 1, italicName)
    addMapping(familyName, 1, 1, bold_italicName)

    base_fonts().update({"normal": getFont(normalName).fontName})
    base_fonts().update({"bold": getFont(boldName).fontName})
    base_fonts().update({"italic": getFont(italicName).fontName})
    base_fonts().update({"bold_italic": getFont(bold_italicName).fontName})


def setFonts(typ):
    """
    Sets fonts for standard font-types

    :param typ: one of sans-serif-afm, serif (sans-serif is default on init)
    :type typ: str
    """
    if typ == 'sans-serif-afm':
        baseNameDict = {
            'Helvetica': "_a______",
            'Helvetica-Bold': "_ab_____",
            'Helvetica-Oblique': "_ai_____",
            'Helvetica-BoldOblique': "_abi____"
        }

        for afm, pfb in baseNameDict.items():
            faceName = afm
            registerFont(faceName, afm, pfb)

        base_fonts().update({
            "normal": pdfmetrics.getFont('Helvetica').fontName
        })
        base_fonts().update({
            "bold": pdfmetrics.getFont('Helvetica-Bold').fontName
        })
        base_fonts().update({
            "italic": pdfmetrics.getFont('Helvetica-Oblique').fontName
        })
        base_fonts().update({
            "bold_italic": pdfmetrics.getFont('Helvetica-BoldOblique').fontName
        })

    elif typ == 'serif':
        setTtfFonts(
            'Calibri',
            __font_dir__,
            normal=('Calibri', 'CALIBRI.TTF'),
            italic=('CalibriBd', 'CALIBRIB.TTF'),
            bold=('CalibriIt', 'CALIBRII.TTF'),
            bold_italic=('CalibriBI', 'CALIBRIZ.TTF'))
