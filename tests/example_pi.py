import os
from cycler import cycler

try:
    import autobasedoc

except:
    import sys
    folder = "../../autobasedoc/"
    __root__ = os.path.dirname(__file__)

    importpath = os.path.realpath(os.path.join(__root__, folder))
    sys.path.append(importpath)


import autobasedoc.autorpt as ar
import autobasedoc.autoplot as ap
from autobasedoc.autorpt import base_fonts, addPlugin

def drawFirstPage(canv, doc):
    """
    This is the Title Page Template (Portrait Oriented)
    """
    canv.saveState()
    #set Page Size
    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame=frame, talkative=True)

    canv.restoreState()

def drawLaterPage(canv, doc):
    """
    This is the Template of any following Portrait Oriented Page
    """
    canv.saveState()
    #set Page Size

    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame=frame)

    canv.restoreState()

def drawLaterSpecialPage(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()

    #set Page Size and
    #some variables

    frame, pagesize = doc.getFrame(doc.template_id)

    #print(pagesize[0],pagesize[1])

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame=frame)

    canv.restoreState()

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
#define page templates

doc = ar.AutoDocTemplate(outname,
                         onFirstPage=(drawFirstPage, 1),
                         onLaterPages=(drawLaterPage,1),
                         onLaterSPages=(drawLaterSpecialPage, 1),
                         leftMargin=0.5*ar.cm,
                         rightMargin=0.5*ar.cm,
                         topMargin=0.5*ar.cm,
                         bottomMargin=0.5*ar.cm,
                         debug=True,
                         producer="NuCOS")

doc.addPageInfo(typ="header",pos="l",
                text="First Header Left",
                image=None,
                line=False,frame="First",
                addPageNumber=False,
                rightMargin=True,
                leftMargin=True,
                shift=None)

doc.addPageInfo(typ="header",
                pos="c",
                text="First Header Center",
                image=None,
                line=False,
                frame="First",
                addPageNumber=False,
                rightMargin=None,
                shift=None)

doc.addPageInfo(typ="header",
                pos="r",
                text="First Header Right",
                image=None,
                line=False,
                frame="First",
                addPageNumber=False,
                rightMargin=None,
                shift=None)

doc.addPageInfo(typ="footer",
                pos="l",
                text="First Footer Left",
                image=None,
                line=False,
                frame="First",
                addPageNumber=False,
                rightMargin=None,
                shift=None)

doc.addPageInfo(typ="footer",
                pos="c",
                text="First Footer Center",
                image=None,
                line=False,
                frame="First",
                addPageNumber=False,
                rightMargin=None,
                shift=None)

doc.addPageInfo(typ="footer",
                pos="r",
                text="First Footer Right",
                image=None,
                line=False,
                frame="First",
                addPageNumber=False,
                rightMargin=None,
                shift=None)

doc.addPageInfo(typ="footer",
                pos="l",
                text="Later Footer Left",
                image=None,
                line=False,
                frame="Later",
                addPageNumber=False,
                rightMargin=False,
                leftMargin=False,
                shift=None)

doc.addPageInfo(typ="footer",
                pos="c",
                text="Later Footer Center",
                image=None,
                line=False,
                frame="Later",
                addPageNumber=False,
                rightMargin=None,
                shift=None)

doc.addPageInfo(typ="footer",
                pos="r",
                text="Later Page Number ",
                image=None,
                line=False,
                frame="Later",
                addPageNumber=True,
                rightMargin=None,
                shift=None)


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
##############################################
content.append(ar.PageBreak())
ar.addHeading("A Table", styles.h1, content)

para = ar.Paragraph(u"My Text that I can write here or take it from somewhere like shown in the next paragraph.", styles.normal)
content.append(para)

content.append(ar.Paragraph("Table is here.",styles.caption))

data = [(1,2,3,4), (5,6,6,8)]

content.append(ar.Table(data, style=None, spaceBefore=10))

## Example 2 adding matplotlib plot
##############################################
content.append(ar.PageBreak())
ar.addHeading("A simple Image", styles.h1, content)
content.append(ar.Paragraph("Pictures are to be placed here.",styles.normal))

title = "My simple plot"

@ap.autoPdfImg
def my_plot1(canvaswidth=5): #[inch]
    fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
    fig.suptitle(title, fontproperties=fontprop)
    x=[1,2,3,4,5,6,7,8]
    y=[1,6,8,3,9,3,4,2]
    ax.plot(x,y,label="legendlabel")
    nrow, ncol = 1, 1
    handles, labels = ax.get_legend_handles_labels()

    leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))

    ax.legend(handles, labels, #labels = tuple(bar_names)
            ncol=ncol, mode=None,
            borderaxespad=0.,
            loc='best',        # the location of the legend handles
            handleheight=None,   # the height of the legend handles
            #fontsize=9,         # prop beats fontsize
            markerscale=None,
            #frameon=False,
            prop=fontprop,
            fancybox=True
            )

    return fig

content.append(my_plot1())
para = ar.Paragraph(" ".join((u"Fig.",str(doc.figcounter()),title)), styles.caption)
content.append(para)

## Example 3 adding matplotlib plot and legend
##############################################
content.append(ar.PageBreak())
ar.addHeading("An Image with Legend", styles.h1, content)
content.append(ar.Paragraph("Pictures are to be placed here.",styles.normal))

title = "My plot with a separate legend"

@ap.autoPdfImage
def my_plot2(canvaswidth=5): #[inch]
    fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
    fig.suptitle(title,fontproperties=fontprop)
    x=[1,2,3,4,5,6,7,8]
    y=[1,6,8,3,9,3,4,2]
    ax.plot(x,y,label="legendlabel")
    nrow, ncol = 1, 1
    handles, labels = ax.get_legend_handles_labels()

    leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))

    leg = leg_fig.legend(handles, labels, #labels = tuple(bar_names)
            ncol=ncol,
            mode=None,
            borderaxespad=0.,
            loc='center',        # the location of the legend handles
            handleheight=None,   # the height of the legend handles
            #fontsize=9,         # prop beats fontsize
            markerscale=None,
            frameon=False,
            prop=fontprop
            #fancybox=True,
            )

    return fig,leg_fig,leg

img, leg = my_plot2()

content.append(leg)
content.append(img)
para = ar.Paragraph(" ".join((u"Fig.",str(doc.figcounter()),title)), styles.caption)
content.append(para)

if __name__ == "__main__":

    doc.multiBuild(content)
