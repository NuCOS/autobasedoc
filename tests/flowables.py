import os
import copy
import autobasedoc.autoplot as ap
import autobasedoc.autorpt as ar

from cycler import cycler
from plot_tools import importSVG
from footer import Footer
from header import Header

from autobasedoc.pdfimage import PdfAsset

plotColors = [
    '#4169E1',  # royalblue
    '#FF6347',  # tomato
    '#FFD700',  # gold
    '#48D1CC',  # mediumturquoise
    '#BA55D3',  # mediumorchid
    '#9ACD36',  # yellowgreen last was 2
    '#DEB887',  # burlywood
    '#2F4F4F',  # darkslategray
    '#FFA500',  # orange
    '#C0C0C0'   # silver
]

# ap.plt.rc('font',family='sans-serif')
ap.plt.rc('axes', prop_cycle=(cycler('color', plotColors)))
fpath = os.path.join('../autobasedoc/fonts', 'calibri.ttf')
font = ap.ft2font.FT2Font(fpath)
ap.fontprop = ap.ttfFontProperty(font)


def get_fontprop(size=None):
    return ap.fm.FontProperties(
        family='sans-serif',
        #name=ap.fontprop.name,
        fname=ap.fontprop.fname,
        size=size,
        stretch=ap.fontprop.stretch,
        style=ap.fontprop.style,
        variant=ap.fontprop.variant,
        weight=ap.fontprop.weight)

customRed = ar.colors.HexColor('#ca656a')  # ar.Color(1.0, 0.2, 0.2)
customYellow = ar.colors.HexColor('#d8d16c')
customLightBlue = ar.colors.HexColor('#e3f6fc') 
customBlue = ar.colors.HexColor('#29a9dc')


styles = ar.Styles()
styles.registerStyles()

PRECOLORS = {
        "green": ar.colors.lightgreen,
        "yellow": customYellow,
        "red": customRed,
        "grey": ar.colors.lightgrey,
        "lightgrey": ar.colors.lightgrey,
        "lightblue": customLightBlue,
        "white": ar.colors.white,
        "whitesmoke": ar.colors.whitesmoke,
        "blue": customBlue
    }

def create_bookmark(text, level):
    return ar.Bookmark(text, level)

def create_image(url, width, height):
    return PdfAsset(url, width=width * ar.cm, height=height * ar.cm)

def create_header(headerText, rightHeaderLines, logoUrl):
    header = Header(headerMarginTop=0.9, debug=False)
    logo = importSVG(
        logoUrl,
        scale=1.0,
        width=60,
        height=110)   # important for scaling inside the header table !
    defaultHeader, reportTitle = header.headerBuild(
        headerText,
        figure_left=logo,
        right_lines=rightHeaderLines)
    return defaultHeader

def create_footer(footerText, footerUrls):
    footer = Footer(footerMarginBottom=0.3, debug=False)
    defaultFooter = footer.footerBuild(
        copy.deepcopy(footerText), footerUrls)
    return defaultFooter

def create_info_table(left_flow=None, right_flow=None, colWidths=[10, 10]):
    body = [[left_flow, right_flow]]
    return create_table(body=body, hTableAlignment="CENTER", centered="all", colWidths=colWidths)

def create_table(body=None,
                     header=None,
                     colWidths=None,
                     hTableAlignment=ar.TA_LEFT,
                     withHLines=True,
                     gridded=False,
                     centered=None,
                     fontsize=12,
                     width=None):
    """
    layout a ldm table (e.g. for result pdf)

    """
    # overwrite some standards (adjust here if needed)
    index = 2
    spaceBefore = 0.0
    spaceAfter = 0.5
    rightPadding = 0.2
    # presetColors = PRECOLORS
    # print(width, colWidths)
    if width is not None:
        if colWidths is None:
            # NOTE if not given, equally spaced
            cols = len(body[0])
            colWidths = [1/cols] * cols
        elif isinstance(colWidths[0], int):
            summe = sum(colWidths)
            colWidths = [x/summe for x in colWidths]
        colWidths = [x*width for x in colWidths]
    styledTable = ar.StyledTable(gridded=gridded)
    if header:
        styledTable.addTableHeader(header, fonttype="italic")
        row_offs = 1
    styledTable.setTableData(body)
    styledTable.addTableExtraStyleCommand(
        ("FONTSIZE", (0, 0), (-1, -1), fontsize))
    styledTable.addTableStyleCommand(('BOTTOMPADDING', (0, 0),
                                        (-1, -1), (fontsize-10)/10.0 * ar.cm))
    if withHLines:
        styledTable.addHorizontalLines(color="black", offsetCol=0)

    if centered is not None:
        # center is asumed to be [(0,0), ...] with row/col pairs
        if centered == "all":
            styledTable.addTableExtraStyleCommand(("ALIGN", (0, 0),
                                        (-1, -1), "CENTER"))
        else:
            for center in centered:
                styledTable.addTableExtraStyleCommand(("ALIGN", center, center, "CENTER"))


    table = styledTable.layoutStyledTable(
        hTableAlignment=hTableAlignment,
        spaceBefore=spaceBefore,
        spaceAfter=spaceAfter,
        rightPadding=rightPadding,
        colWidths=colWidths)
    return table

def create_img_table(body=None,
                   colWidths=None,
                   hTableAlignment=ar.TA_CENTER,
                   gridded=False):
    """
    layout a ldm table (e.g. for result pdf)

    """
    # overwrite some standards (adjust here if needed)
    index = 2
    spaceBefore = 0.0
    spaceAfter = 0.5
    rightPadding = 0.2
    styledTable = ar.StyledTable(gridded=gridded)
    styledTable.setTableData(body)
    styledTable.addTableExtraStyleCommand(("ALIGN", (0,0), (-1,-1), "CENTER"))
    styledTable.addHorizontalLines(color="blue", offsetCol=0)
    table = styledTable.layoutStyledTable(
        hTableAlignment=hTableAlignment,
        spaceBefore=spaceBefore,
        spaceAfter=spaceAfter,
        rightPadding=rightPadding,
        colWidths=colWidths)
    return table


def create_paragraph(bookmark, bookmarklevel, text, fontsize):
    return ar.Paragraph(text, styles.title)

def create_vertical_spacer(height):
    return ar.Spacer(width=2.0 * ar.cm, height=height * ar.cm)


def create_figure(xx=None, yy=None, hAlign="CENTER", title="", legend="", width=5):
    """
    this wrapping adds just the hAlign attribute
    """
    fig, leg = figure(xx=xx, yy=yy, title=title, legend=legend, width=width)
    if hAlign:
        fig.hAlign = hAlign
        leg.hAlign = hAlign
    return fig, leg

@ap.autoPdfImage
def figure(xx=None, yy=None, title="", legend="", width=5):  #[inch]
    """
    plot an example figure with matplotlib
    
    """
    fig, ax = ap.plt.subplots() #figsize=(canvaswidth, canvaswidth)
    fig.suptitle(title, fontproperties=get_fontprop(16))
    if xx is None:
        xx = [1, 2, 3, 4, 5, 6, 7, 8]
    if yy is None:
        yy = [1, 6, 8, 3, 9, 3, 4, 2]
    ax.plot(xx, yy, label=legend)
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
        prop=get_fontprop(12) # can be distinct
        #fancybox=True,
    )
    return fig, leg_fig, leg

@ap.autoPdfImg
def my_plot(xx=None, yy=None, width=5): #[inch]
    fig, ax = ap.plt.subplots(figsize=(width,width))
    fig.suptitle("My Plot",fontproperties=fontprop)
    if xx is None:
        xx = [1, 2, 3, 4, 5, 6, 7, 8]
    if yy is None:
        yy = [1, 6, 8, 3, 9, 3, 4, 2]
    ax.plot(xx,yy,label="legendlabel")
    nrow,ncol=1,1
    handles, labels = ax.get_legend_handles_labels()

    leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))

    ax.legend(handles, labels, #labels = tuple(bar_names)
            ncol=ncol, mode=None,
            borderaxespad=0.,
            loc='center',        # the location of the legend handles
            handleheight=None,   # the height of the legend handles
            #fontsize=9,         # prop beats fontsize
            markerscale=None,
            frameon=False,
            prop=fontprop
            #fancybox=True,
            )

    return fig

