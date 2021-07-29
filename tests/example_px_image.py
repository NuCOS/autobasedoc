"""
basic examples
"""

try:
    import autobasedoc

except:
    import os, sys
    folder = "../../autobasedoc/"
    __root__ = os.path.dirname(__file__)

    importpath = os.path.realpath(os.path.join(__root__, folder))
    sys.path.append(importpath)

## Example prerequisites
import os
from cycler import cycler
from autobasedoc import autorpt as ar
from autobasedoc import autoplot as ap

from autobasedoc.pdfimage import convert_px_to_pdf_image_obj, PdfImage

ar.setTtfFonts(
    'Calibri',
    os.path.realpath(ar.__font_dir__),
    normal=('Calibri', 'calibri.ttf'),
    bold=('CalibriBd', 'calibrib.ttf'),
    italic=('CalibriIt', 'calibrii.ttf'),
    bold_italic=('CalibriBdIt', 'calibriz.ttf'))

plotColorDict = dict(
    royalblue='#4169E1',
    tomato='#FF6347',
    gold='#FFD700',
    mediumturquoise='#48D1CC',
    mediumorchid='#BA55D3',
    yellowgreen='#9ACD32',
    burlywood='#DEB887',
    darkslategray='#2F4F4F',
    orange='#FFA500',
    silver='#C0C0C0')

plotColorNames = list(plotColorDict.keys())
plotColors = list(plotColorDict.values())

ap.plt.rc('axes', prop_cycle=(cycler('color', plotColors)))

fpath = os.path.join(ar.__font_dir__, 'calibri.ttf')
font = ap.ft2font.FT2Font(fpath)
ap.fontprop = ap.ttfFontProperty(font)

img_path = "grafics/color_logo.png"

fontprop = ap.fm.FontProperties(
    family='sans-serif',
    fname=ap.fontprop.fname,
    size=None,
    stretch=ap.fontprop.stretch,
    style=ap.fontprop.style,
    variant=ap.fontprop.variant,
    weight=ap.fontprop.weight)

fontsize = 10
ap.matplotlib.rcParams.update({
    'font.size': fontsize,
    'font.family': 'sans-serif'
})

styles = ar.Styles()
styles.registerStyles()

outname = os.path.join(os.path.dirname(__file__), "MinimalExample.pdf")
# from django.http import HttpResponse
# outname = HttpResponse(mimetype='application/pdf')
# outname['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

doc = ar.AutoDocTemplate(outname,onFirstPage=ar.onFirstPage,onLaterPages=ar.onLaterPages,onLaterSPages=ar.onLaterPages,
                        leftMargin=0.5*ar.cm, rightMargin=0.5*ar.cm, topMargin=0.5*ar.cm, bottomMargin=0.5*ar.cm)

content = []

#add title
para = ar.Paragraph(u"Minimal Example Title", styles.title)
content.append(para)
content.append(ar.PageBreak())

# Create Table Of Contents. Override the level styles (optional)
# and add the object to the story
toc = ar.doTabelOfContents()
content.append(ar.Paragraph(u"Inhaltsverzeichnis", styles.h1))
content.append(toc)


## Example 1 adding a table
content.append(ar.PageBreak())
ar.addHeading("A Table", styles.h1, content)

para = ar.Paragraph(u"My Text that I can write here or take it from somewhere like shown in the next paragraph.", styles.normal)
content.append(para)

content.append(ar.Paragraph("Table is here.",styles.caption))

image_pdf = PdfImage(convert_px_to_pdf_image_obj(img_path),width=1*ar.cm,height=1*ar.cm)

data = [(image_pdf,2,3,4),]

content.append(ar.Table(data, style=None, spaceBefore=10))

## Finally

doc.multiBuild(content)
