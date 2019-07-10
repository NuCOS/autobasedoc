"""
autorpt
=======

.. module:: autorpt
   :platform: Unix, Windows
   :synopsis: document templates for automatic document generation

.. moduleauthor:: Johannes Eckstein

Class AutoDocTemplate customized for automatic document creation
this inherits and partly redefines reportlab code

"""
from __future__ import print_function

import os
import sys
import random
import string
from hashlib import sha1
from operator import attrgetter
from itertools import count
from collections import OrderedDict

from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, cm, mm  #,pica

from reportlab.platypus import (Image, Paragraph, PageBreak, Table, Spacer,
                                Flowable, KeepTogether, FrameBreak, PageBegin)

from reportlab.platypus.doctemplate import (
    BaseDocTemplate, PageTemplate, NextPageTemplate, _doNothing, LayoutError,
    ActionFlowable, FrameActionFlowable, _addGeneratedContent, _fSizeString,
    NullActionFlowable, NotAtTopPageBreak)

from reportlab.platypus.frames import Frame
from reportlab.platypus.flowables import SlowPageBreak, DDIndenter, PageBreakIfNotEmpty
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle

# configure pdf producer
from reportlab.pdfbase.pdfdoc import PDFInfo

# module imports
from autobasedoc import base_fonts, color_dict, colors
import autobasedoc.autoplot as ap
from autobasedoc.styledtable import StyledTable
from autobasedoc.styles import StyleSheet, Styles
from autobasedoc.pageinfo import addPlugin, PageInfo
from autobasedoc.fonts import registerFont, setFonts, setTtfFonts, getFont
from autobasedoc.tableofcontents import AutoTableOfContents

_baseFontNames = base_fonts()
_color_dict = color_dict()
_basePath = os.path.realpath(os.path.dirname(__file__))

sys.path.append(_basePath)

# #TODO: cx Freeze, this needs adoption to your version of cx_freeze
# if _basePath.endswith("library.zip"):
#     _basePath = os.path.realpath(os.path.join(_basePath, '../'))

__font_dir__ = os.path.realpath(os.path.join(_basePath, "fonts"))
#__assets_dir__ = os.path.realpath(os.path.join(_basePath,"assets"))

def reprFrame(frame):
    _dict = vars(frame)
    for key in sorted(list(_dict.keys())):
        print(key, ": ", _dict[key])

# Here are some template files, you should define your own:

def drawFirstPortrait(canv, doc):
    """
    This is the Title Page Template (Portrait Oriented)
    """
    canv.saveState()
    #set Page Size
    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame="First")

    canv.restoreState()

def drawFirstLandscape(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page

    the frame object is only used as a reference to be able to draw to the canvas

    After creation a Frame is not usually manipulated directly by the
    applications program -- it is used internally by the platypus modules.

    Here is a diagramatic abstraction for the definitional part of a Frame::

                width                    x2,y2
        +---------------------------------+
        | l  top padding                r | h
        | e +-------------------------+ i | e
        | f |                         | g | i
        | t |                         | h | g
        |   |                         | t | h
        | p |                         |   | t
        | a |                         | p |
        | d |                         | a |
        |   |                         | d |
        |   +-------------------------+   |
        |    bottom padding               |
        +---------------------------------+
        (x1,y1) <-- lower left corner

    NOTE!! Frames are stateful objects.  No single frame should be used in
    two documents at the same time (especially in the presence of multithreading.
    """
    canv.saveState()
    #set Page Size
    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame="First")

    canv.restoreState()

onFirstPage = drawFirstPortrait, 0

def drawLaterPortrait(canv, doc):
    """
    This is the Template of any following Portrait Oriented Page
    """
    canv.saveState()
    #set Page Size

    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()

def drawLaterLandscape(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()

    #set Page Size and
    #some variables

    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()

onLaterPages = drawLaterPortrait, 0

def drawLaterSpecialPortrait(canv, doc):
    """
    This is the Template of any following Portrait Oriented Page
    """
    canv.saveState()
    #set Page Size

    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()

def drawLaterSpecialLandscape(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()

    #set Page Size and
    #some variables

    frame, pagesize = doc.getFrame(doc.template_id)

    canv.setPageSize(pagesize)
    canv.setFont(base_fonts()["normal"], doc.fontSize)

    addPlugin(canv, doc, frame="Later")

    canv.restoreState()

onLaterSPages = drawLaterSpecialLandscape, 0

class AutoDocTemplate(BaseDocTemplate):
    """
    This is our Document Template, here we want to add our special formatting, that we need for our Document Creation

    We derive from BaseDocTemplate, we don't want to and cannot superclass here...

    We have one unique way inside afterFlowable to create one outline entry for each flowable by:

    - adding the <a name=outlineName> to text within the paragraph flowable.
    - using self.notify(), self.canv.bookmarkPage() and self.canv.addOutlineEntry() inside a function afterFlowable() which is overloaded in an own Template class that inherits from BaseDocTemplate

    For a basic example, please see in TOC with clickable links by rptlab.
    we implemented a special action flowable class called Bookmark, that has no actions! please see modifications in afterFlowable().
    Unlike with paragraphs we are also abled to store many outline entries from one Table.
    This is the best way to do this for multible bookmarks in one table flowable without having to write too much overhead code.

    We discovered this workaround that was postet in ReportLab-users Group back in 2004 by Marc Stober. This workaround suggests using a class Bookmark.
    We have ported this to use an ActionFlowable, to do the bookmarking, because this flowable is not doing anything at all, but storing some values, so that afterFlowable() can see them.

    To define Template settings for your pages you can use three stages, override the default values::

        onFirstPage=(_doNothing, 0)
        onLaterPages=(_doNothing, 0)
        onLaterSPages=(_doNothing, 0)

    The stages are:

    - `onFirstPage` template for the first page
    - `onLaterPages` template of any following page
    - `onLaterSPages` template on any later switchable special page

    Instead of `_doNothing`, a function that just carries a pass, you can define your own function that can draw something on the canvas before anything else gets drawn.
    For the most common cases there are the following 'template' functions:

    - :func:`drawFirstPortrait`
    - :func:`drawFirstLandscape`
    - :func:`drawLaterPortrait`
    - :func:`drawLaterLandscape`
    - :func:`drawLaterSpecialPortrait`
    - :func:`drawLaterSpecialLandscape`

    To define a scheme, where all pages are Portrait but special pages are landscape pages::

        onFirstPage=onFirstPage
        onLaterPages=onLaterPages
        onLaterSPages=onLaterSPages

    """

    def __init__(self,
                 filename,
                 onFirstPage=(_doNothing, 0),
                 onLaterPages=(_doNothing, 0),
                 onLaterSPages=(_doNothing, 0),
                 templates = [],
                 leftMargin=0.5 * cm,
                 rightMargin=0.5 * cm,
                 topMargin=0.5 * cm,
                 bottomMargin=0.5 * cm,
                 title=None,
                 author=None,
                 subject=None,
                 producer=None,
                 creator=None,
                 keywords=[],
                 debug=False):

        if producer is not None:
            PDFInfo.producer = producer

        super(AutoDocTemplate, self).__init__(filename,
            pagesize=A4,
            leftMargin=leftMargin,
            rightMargin=rightMargin,
            topMargin=topMargin,
            bottomMargin=bottomMargin,
            title=title,
            author=author,
            subject=subject,
            producer=producer,
            creator=creator,
            keywords=keywords)

        self.debug = debug
        if self.debug:
            self.showBoundary = 1
        else:
            self.showBoundary = 0

        #Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='F1')

        # can be Landscape or Portrait
        self.onFirstPage, self.framesFirst = onFirstPage
        # Later Portrait or Landscape
        self.onLaterPages, self.framesLater = onLaterPages
        # Later Landscape to change the Format from Landscape to Portrait or vice versa
        self.onLaterSPages, self.framesLaterS = onLaterSPages

        self.bottomTableHeight = 0

        self.figCount = 0
        self.PageDecorated = False

        self.pageInfos = OrderedDict()

        self.lineWidth = 0.15
        self.fontSize = 12
        self.topM = self.fontSize * 0.77
        self.bottomM = self.fontSize - self.topM
        self.templates={}

        self.templates_maker()

        if self.debug:
            print("PDF Inhalte werden erzeugt...")
            print("on First Page: ", (onFirstPage))
            print("on Later Pages: ", (onLaterPages))
            print("on Later Special Pages: ", (onLaterSPages))

    @property
    def template_id(self):
        return sys._getframe(1).f_code.co_name.strip("draw")

    def templates_maker(self):
        """
        Here we populate the page templates (register page templates and functions)
        Page templates are separated into three stages:

        - on first page
        - on later page
        - on later special page

        using a list, that simplified looks like this::

            [PageTemplate(id='First',
                          frames=[firstFrame0, firstFrame1, firstFrame2],
                          onPage=onFirstPage,
                          pagesize=self.pagesize),
             PageTemplate(id='Later',
                          frames=[laterFrame0, laterFrame1, laterFrame2],
                          onPage=onLaterPages,
                          pagesize=self.pagesize),
             PageTemplate(id='Special',
                          frames=[specialFrame0, specialFrame1, specialFrame2],
                          onPage=onLaterSPages,
                          pagesize=self.pagesize)])

        the list is sent to::

            BaseDocTemplate.addPageTemplates(list)

        the templates are later accessible by::

            self.pageTemplates[index]

        in self.handle_pageBegin() the next page automatically becomes the first
        'Later' flowable

        to controll switching on the next page template use
        self.PageNext e.g::

            nextTemplate = self.doc.getSpecialTemplate(temp_name="")
            ar.PageNext(self.contents, nextTemplate=nextTemplate)

        """
        template_name = lambda x: attrgetter("__name__")(x).strip("draw")
        ### on first page
        frame_count = self.framesFirst
        template_id = template_name(self.onFirstPage)
        pagesizeL=False
        if self.onFirstPage is not _doNothing:
            if template_id.startswith("First"):
                if template_id.endswith("Portrait"):
                    pagesizeL=False
                elif template_id.endswith("Landscape"):
                    pagesizeL=True

        self.templates.update({template_id:
            self.getMultiColumnTemplate(frameCount=frame_count,
                                        template_id=template_id,
                                        onPage_template_func=self.onFirstPage,
                                        pagesize_landscape=pagesizeL)})

        ### on later page
        frame_count = self.framesLater
        template_id = template_name(self.onLaterPages)
        pagesizeL=False
        if self.onLaterPages is not _doNothing:
            if template_id.startswith("Later"):
                if template_id.endswith("Portrait"):
                    pagesizeL=False
                elif template_id.endswith("Landscape"):
                    pagesizeL=True

        self.templates.update({template_id:
            self.getMultiColumnTemplate(frameCount=frame_count,
                                        template_id=template_id,
                                        onPage_template_func=self.onLaterPages,
                                        pagesize_landscape=pagesizeL)})

        ### on later special page
        frame_count = self.framesLaterS
        template_id = template_name(self.onLaterSPages)
        pagesizeL=False
        if self.onLaterSPages is not _doNothing:
            if template_id.endswith("Portrait"):
                pagesizeL=False
            elif template_id.endswith("Landscape"):
                pagesizeL=True

        self.templates.update({template_id:
            self.getMultiColumnTemplate(frameCount=frame_count,
                                        template_id=template_id,
                                        onPage_template_func=self.onLaterSPages,
                                        pagesize_landscape=pagesizeL)})

        self.addPageTemplates(list(self.templates.values()))


    def createFrame(self, frame_id="Portrait",
                    x1=0.,
                    y1=0.,
                    width=0.,
                    height=0.,
                    left_padding=0.,
                    bottom_padding=0.,
                    right_padding=0.,
                    top_padding=0.,
                    overlap=None):
        """
        Frame reportlab internal signature::

                        width                    x2,y2
                +---------------------------------+
                | l  top_padding                r | h
                | e +-------------------------+ i | e
                | f |                         | g | i
                | t |                         | h | g
                |   |                         | t | h
                | p |                         |   | t
                | a |                         | p |
                | d |                         | a |
                |   |                         | d |
                |   +-------------------------+   |
                |    bottom padding               |
                +---------------------------------+
                (x1,y1) <-- lower left corner

        """
        def makeRandomId(length=3, chars=string.ascii_lowercase):
            """
            create a file id of lower case ascii characters with length
            """
            return ''.join(random.choice(chars) for _ in range(length))

        return Frame(x1, y1, width, height,
                     leftPadding=left_padding,
                     bottomPadding=bottom_padding,
                     rightPadding=right_padding,
                     topPadding=top_padding,
                     id=f"{frame_id}_{makeRandomId()}",
                     showBoundary=self.showBoundary,
                     overlapAttachedSpace=overlap,
                     _debug=None)

    def getFrame(self, temp_name=None, orientation=None, last=False):
        """
        returns frame

        to get the master frame inside the pageTemplates

        use orientation=None keyarg (default)

        frame._x1,frame._y1
        frame._width,frame._height
        frame._leftPadding,frame._bottomPadding
        frame._rightPadding,frame._topPadding
        and pagesize:
        (x,y)
        """

        f = attrgetter("id")
        frame = None

        if temp_name is not None:

            pageTemplate = self.getTemplate(temp_id=temp_name, last=last)

        else:
            if last:
                try:
                    pageTemplate = self.pageTemplates[-1]
                except:
                    frame = None
            else:
                try:
                    pageTemplate = self.pageTemplates[0]
                except:
                    frame = None

        # to get the master frame
        if orientation is None:
            orientation = temp_name

        for frame in pageTemplate.frames:
            #print(f(frame))
            if f(frame).startswith(orientation):
                return frame, pageTemplate.pagesize

        if frame is None:
            print("Error occured accessing self.pageTemplates", temp_name)
            raise Exception
            #            #print ( thisTemplate.frames[0].id )
            #            return thisTemplate.frames[0],thisTemplate.pagesize
            #
            #        else:


    def getTemplate(self, temp_id=None, last=False, as_name=False):
        """
        Return first page template with an id that starts with frame_name
        """
        f = attrgetter("id")
        template = None

        if not last:
            for temp in self.pageTemplates:
                if f(temp).startswith(temp_id):
                    template = temp
                    break

        else:
            for temp in self.pageTemplates[::-1]:
                if f(temp).startswith(temp_id):
                    template = temp
                    break

        if as_name and template:
            template = f(template)

        if template is None:
            print(f"Error from {self.template_id}: temp_id:{temp_id}, last:{last}, as_name:{as_name}")

        return template

    def getSpecialTemplate(self, temp_name="Later"):
        """
        get the next page action flowable template that starts with temp_name
        """
        return NextPageTemplate(self.getTemplate(temp_id=temp_name, last=True, as_name=True))

    def getMultiColumnTemplate(self,
                               frameCount=0,
                               template_id="LaterL",
                               onPage_template_func=_doNothing,
                               pagesize_landscape=False):
        """
        create a TwoColumn Frame

        This is customized for landscape format pages.
        if you want portrait, set pagesizeL to False

        Frame vals::

            x1,
            y1,
            width,
            height,
            leftPadding=6,
            bottomPadding=6,
            rightPadding=6,
            topPadding=6,
            id=None,
            showBoundary=0,
            overlapAttachedSpace=None,
            _debug=None

        Template Style for Two Frames::

                    width          (x2,y2)
            +-----------------------------+-----------------------------+
            | l  top padding            r | h                           |
            | e +---------------------+ i | e +---------------------+   |
            | f |                     | g | i |                     |   |
            | t |                     | h | g |                     |   |
            |   |                     | t | h |     Second          |   |
            | p |                     |   | t |     frame           |   |
            | a |                     | p |   |                     |   |
            | d |                     | a |   |                     |   |
            |   |                     | d |   |                     |   |
            |   +---------------------+   |   +---------------------+   |
            |    bottom padding           |                             |
            +-----------------------------+-----------------------------+
            (x1,y1) <-- lower left corner

        """
        #self._calc()
        if pagesize_landscape:
            width, height = landscape(self.pagesize)
            fF = "Landscape"
        else:
            width, height = self.pagesize
            fF = "Portrait"

        fullWidth = width - (self.leftMargin + self.rightMargin)

        #print(f">>>> {frameCount} {fF} fullWidth: {fullWidth} width={width} left={self.leftMargin} right={self.rightMargin}")

        frameHeight = height - (self.bottomMargin + self.topMargin)
        frames = []
        #construct a frame for each column

        if frameCount > 0:
            frameWidth = fullWidth / float(frameCount)

            for frame in range(frameCount):
                leftMargin = self.leftMargin + frame * frameWidth
                #print(">>>>>>>>", leftMargin, frameWidth)
                frames.append(self.createFrame(frame_id=f"{fF}{frame}",
                                          x1=leftMargin,
                                          y1=self.bottomMargin,
                                          width=frameWidth,
                                          height=frameHeight,
                                          left_padding=0.,
                                          bottom_padding=0.,
                                          right_padding=0.,
                                          top_padding=0.,
                                          overlap=None))

            frames.append(self.createFrame(frame_id=template_id,
                                      x1=0.,
                                      y1=0.,
                                      width=width,
                                      height=height,
                                      left_padding=0.,
                                      bottom_padding=0.,
                                      right_padding=0.,
                                      top_padding=0.,
                                      overlap=None))
        else:
            frames.append(self.createFrame(frame_id=template_id,
                                      x1=self.leftMargin,
                                      y1=self.bottomMargin,
                                      width=fullWidth,
                                      height=frameHeight,
                                      left_padding=0.,
                                      bottom_padding=0.,
                                      right_padding=0.,
                                      top_padding=0.,
                                      overlap=None))

        return PageTemplate(id=template_id,
                            frames=frames,
                            onPage=onPage_template_func,
                            pagesize=(width, height))

    def updatePageInfo(self, pI):
        """
        addPageInfo, using the PageInfo type object

        :param pI: PageInfo() object
        """
        typ = pI.typ

        if pI.line:
            typ += "_"
        if not pI.image is None:
            typ += "___"
        if not pI.text is None:
            typ += "____"
        pI.typ = typ
        self.pageInfos.update({pI.frame + pI.typ + pI.pos: pI})

    def addPageInfo(self,
                    typ="header",
                    pos="l",
                    text=None,
                    image=None,
                    line=False,
                    frame="First",
                    addPageNumber=False,
                    rightMargin=None,
                    leftMargin=None,
                    topMargin=None,
                    bottomMargin=None,
                    shift=None):
        """
        add header and footer elements, that raster into the frame::

                l            c            r

            +---------------------------------+
            | l  header                     r |
            | e +------------+------------+ i |
            | f |                         | g |
            | t |                         | h |
            |   |                         | t |
            | p |                         |   |
            | a |                         | p |
            | d |                         | a |
            |   |                         | d |
            |   +------------+------------+   |
            |    footer                       |
            +---------------------------------+

        :param frame: "First"/"Later"
        :param typ: header/footer
        :param pos: "l"/"c"/"r"
        :param text: ""
        :param image: preferrably a PDF Image
        :param addPageNumber: True/False
        :param rightMargin: shift of 'r' ancor towards centre (only for line).
        :param shift: shifts the image in (x,y) direction (only for image).
        :param line: True/False if true, draw a line from 'l' to 'r'

        creates a PageInfo object:
            PageInfo(typ,pos,text,image,line,frame,addPageNumber,rightMargin,shift)

        As of now we consider either text or image and optionaly a line
        and will not handle these cases separately.
        """
        self.updatePageInfo(
            PageInfo(typ, pos, text, image, line, frame, addPageNumber,
                     rightMargin=rightMargin, leftMargin=leftMargin,
                     topMargin=topMargin, bottomMargin=bottomMargin,
                     shift=shift))

    def scaleImage(self, thisImage, scaleFactor=None):
        """
        Function to allow user scaling of factor.
        A scaling greater than 0, lesser than 1 is
        allowed. By default a scaling of 0.7071 is
        applied to thisImage
        """
        if scaleFactor is None:
            setattr(thisImage, "_userScaleFactor", 0.7071)
            #thisImage._userScaleFactor=(1./np.sqrt(2))
        else:
            #if scaleFactor<=1.:
            #   thisImage._userScaleFactor=scaleFactor
            setattr(thisImage, "_userScaleFactor", scaleFactor)

        return thisImage

    def _scaleApply(self, Img, scaling):
        """
        scales width and height of an Image
        """
        Img.drawWidth = Img.drawWidth * scaling
        Img.drawHeight = Img.drawHeight * scaling

        return Img

    def handle_pageBegin(self):
        """
        override base method to add a change of page template after the firstpage.
        by default: use Later template
        """
        self._handle_pageBegin()
        template = self.getTemplate(temp_id='Later', as_name=True)
        self._handle_nextPageTemplate(template)

    def handle_flowable(self, flowables):
        """
        overriding base method!!!

        try to handle one flowable from the front of list flowables.

        added a dirty workaround to scale images
        if their boundingBox exceeds the borders of the frame.
        """

        #allow document a chance to look at, modify or ignore
        #the object(s) about to be processed
        self.filterFlowables(flowables)
        self.handle_breakBefore(flowables)
        self.handle_keepWithNext(flowables)
        f = flowables[0]
        del flowables[0]
        if f is None:
            return
        if isinstance(f, PageBreak):
            npt = f.nextTemplate
            if npt and not self._samePT(npt):
                npt = NextPageTemplate(npt)
                npt.apply(self)
                self.afterFlowable(npt)
            if isinstance(f, SlowPageBreak):
                self.handle_pageBreak(slow=1)
            else:
                #print( f.__class__.__name__, self.frame.id )
                self.handle_pageBreak()
            self.afterFlowable(f)
        elif isinstance(f, ActionFlowable):
            f.apply(self)
            self.afterFlowable(f)
        else:
            frame = self.frame
            canv = self.canv
            if self.debug:
                frame.drawBoundary(canv)
            #handle scaling to fit a PdfImage on self.frame
            if isinstance(f, Table):
                pass  # controls default behaviour for Table typed flowables
                #f.setStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.black)])
            elif isinstance(f, Spacer):
                pass
            if isinstance(f, ap.PdfImage):
                #print("height of image:",f.drawHeight)
                #print("height of frame:",frame._aH)
                xfactor = getattr(f, "_userScaleFactor", None)
                factor = 1.

                if xfactor is not None:
                    #print( "applying scale", xfactor)
                    factor = xfactor
                    f = self._scaleApply(f, factor)
                    setattr(f, "_userScaleFactor", None)

                #resizing image if drawWidth is exceeding the available frame Width _aW
                if f.drawWidth > frame._aW:
                    factor = frame._aW / f.drawWidth
                    f = self._scaleApply(f, factor)
                    if self.debug:
                        print("PdfImage exceeds available width on frame:",
                              frame.id, frame._aW / cm, frame._aH / cm,
                              f.drawWidth / cm, f.drawHeight / cm,
                              "rescaling to fit frame geometry.")

                #resizing image if drawHeight is exceeding the available frame Width _aH
                if f.drawHeight > frame._aH:

                    #print("PdfImage height exceeds height of available space on frame:",
                    #      frame.id,
                    #      "rescaling to fit frame geometry..." )

                    factor = frame._aH / f.drawHeight
                    f = self._scaleApply(f, factor)
                #print("spaceBelow:",frame._aH-f.drawHeight )
                #print("spaceBesides:",frame._aW-f.drawWidth )
                #print(f.drawHeight)

                #try to fit it then draw it
            if frame.add(f, canv, trySplit=self.allowSplitting):
                if not isinstance(f, FrameActionFlowable):
                    self._curPageFlowableCount += 1
                    self.afterFlowable(f)
                _addGeneratedContent(flowables, frame)
            else:
                if self.allowSplitting:
                    # see if this is a splittable thing
                    S = frame.split(f, canv)
                    n = len(S)
                else:
                    n = 0
                if n:
                    if not isinstance(S[0], (PageBreak, SlowPageBreak,
                                             ActionFlowable, DDIndenter)):
                        if not frame.add(S[0], canv, trySplit=0):
                            ident = "Splitting error(n==%d) on page %d in\n%s\nS[0]=%s" % \
                            (n,
                             self.page,
                             self._fIdent(f, 60, frame),
                             self._fIdent(S[0], 60, frame))
                            #leave to keep apart from the raise
                            raise LayoutError(ident)
                        self._curPageFlowableCount += 1
                        self.afterFlowable(S[0])
                        flowables[0:0] = S[
                            1:]  # put rest of splitted flowables back on the list
                        _addGeneratedContent(flowables, frame)
                    else:
                        flowables[
                            0:0] = S  # put splitted flowables back on the list
                else:
                    if hasattr(f, '_postponed'):
                        pass
                        #print( f.__class__.__name__, self.frame.id, f.drawWidth, f.drawHeight, )

                        # ident = "Flowable %s%s too large on page %d in frame %r%s of template %r" % \
                        # (self._fIdent(f, 60, frame),
                        #  _fSizeString(f),
                        #  self.page,
                        #  self.frame.id,
                        #  self.frame._aSpaceString(),
                        #  self.pageTemplate.id)
                        # #leave to keep apart from the raise
                        # raise LayoutError(ident)
                    # this ought to be cleared when they are finally drawn!
                    f._postponed = 1
                    mbe = getattr(self, '_multiBuildEdits', None)
                    if mbe:
                        mbe((delattr, f, '_postponed'))
                    # put the flowable back
                    flowables.insert(0, f)
                    self.handle_frameEnd()


    def afterFlowable(self, flowable):
        """
        Registers TOC entries.
        and outline entries

        Entries to the table of contents can be done either manually by
        calling the addEntry method on the TableOfContents object or automatically
        by sending a 'TOCEntry' notification in the afterFlowable method of
        the DocTemplate you are using. The data to be passed to notify is a list
        of three or four items containing a level number, the entry text, the page
        number and an optional destination key which the entry should point to.
        This list will usually be created in a document template's method like
        afterFlowable(), making notification calls using the notify() method
        with appropriate data.
        """
        try:
            cln = flowable.cln()

        except:
            cln = ""

        if cln.startswith("Header"):
            pass

        if cln.startswith("Footer"):
            pass

        if cln.startswith("Bookmark"):
            #print("Bookmark",flowable.title,"created at level:",flowable.level)

            #This seems to be not necessary
            entity_info = flowable.level, flowable.title, self.page, flowable.key
            self.notify('TOCEntry', entity_info)

            self.currSpaceToBottom = self.frame._y + self.frame._y1p  # <-- not necessary

            self.canv.bookmarkPage(flowable.key,
                                   fit='XYZ',
                                   top=self.currSpaceToBottom)
            ##            if flowable.fullpage:
            ##                flowable.key='Diagramm'+flowable.key
            #self.canv.bookmarkPage(flowable.key, fit='FitH', top=800)
            #self.canv.bookmarkPage(flowable.key, fit='XYZ')

            # print(self.getFrame()[1][1])

            self.canv.addOutlineEntry(
                flowable.title,
                flowable.key,
                level=flowable.level,
                closed=True)
            self.canv.showOutline()


    # def build(self, flowables):
    #     """
    #     build the document using the flowables.  Annotate the first page using the onFirstPage
    #     function and later pages using the onLaterPages function.  The onXXX pages should follow
    #     the signature::
    #         def myOnFirstPage(canvas, document):
    #             # do annotations and modify the document
    #             ...
    #     The functions can do things like draw logos, page numbers,
    #     footers, etcetera. They can use external variables to vary
    #     the look (for example providing page numbering or section names).
    #     """
    #     self._calc()  #in case we changed margins sizes etc
    #     AutoDocTemplate.build(self, flowables)
    #     self.PageDecorated = True


    def figcounter(self):
        """
        a simple figure counter, this is a very dirty way
        to control the number of figures
        """
        self.figCount += 1
        return str(self.figCount)


class BottomSpacer(Spacer):
    """
    a spacer that fills the current doc unto the bottom
    """
    def wrap(self, availWidth, availHeight):
        height = availHeight - self._doc.bottomTableHeight

        if height <= 0:
            return (self.width, availHeight)
        else:
            return (self.width, height)


def doTabelOfContents():
    """
    returns toc with 3 customized headings level styles
    """
    toc = AutoTableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            fontSize=12,
            name='TOCHeading1',
            leftIndent=4,
            firstLineIndent=0,
            spaceBefore=0,
            leading=13),
        ParagraphStyle(
            fontSize=10,
            name='TOCHeading2',
            leftIndent=8,
            firstLineIndent=0,
            spaceBefore=0,
            leading=11),
        ParagraphStyle(
            fontSize=9,
            name='TOCHeading3',
            leftIndent=12,
            firstLineIndent=0,
            spaceBefore=0,
            leading=10),
        ]
    return toc


class Header(NullActionFlowable):
    _ids = count(0)

    def __init__(self):
        super(Header, self).__init__()
        self._id = self._ids.__next__()

    @classmethod
    def cln(cls):
        return cls.__name__

    @property
    def id(self):
        return str(self._id)


class Footer(NullActionFlowable):
    _ids = count(0)

    def __init__(self):
        super(Footer, self).__init__()
        self._id = self._ids.__next__()

    @classmethod
    def cln(cls):
        return cls.__name__

    @property
    def id(self):
        return str(self._id)


class Bookmark(NullActionFlowable):
    """
    Utility class to display PDF bookmark.

    :param title: Title of the bookmark
    :param level: Level entry in the outline

    """
    _ids = count(0)

    def __init__(self, title, level=0):
        super(Bookmark, self).__init__()
        self.title = title
        self._level = level
        self._id = self._ids.__next__()
        self.key = self.createBookmarkKey()

    @classmethod
    def cln(cls):
        return cls.__name__

    @property
    def level(self):
        return self._level

    @property
    def id(self):
        return str(self._id)

    def createBookmarkKey(self):
        """
        creates a Bookmark Key using title, level
        and the identity of this ActionFlowable
        """
        key = f"{self.title}{self.level}{self.id}".encode(encoding="utf-8")
        return sha1(key).hexdigest()


def getBookmarkLast(contents):
    """
    return last bookmark in contents or None
    """
    for f in contents[::-1]:
        if isinstance(f, Bookmark):
            return f


def getBaseFont(fonttype):
    if fonttype in base_fonts():
        return base_fonts()[fonttype]


def doHeading(title, sty, outlineText=None, bookmarkFullpage=False):
    """
    function that makes a Flowable for a heading
    :param title: title of the paragraph
    :param sty: style for the paragraph
    :param outlineText: with specifying an "ancortext" we can control the output to the bookmark name in the outline of the PDF
    """

    if outlineText is None:
        outlineText = title

    style = sty.name
    if style == 'Heading1':
        level = 0
    elif style == 'Heading2':
        level = 1
    elif style == 'Heading3':
        level = 2
    else:
        level = 0

    bm = Bookmark(outlineText, level)

    #create bookmarkname
    key = bm.key
    an = '<a name="%s"/>' % key
    if bookmarkFullpage:
        h = Paragraph(title, sty)
    else:
        h = Paragraph(an + title, sty)

# heading must stay with next paragraph or table
##    h.keepWithNext = True
    return (bm, h)


def addHeading(title, sty, page):
    """
    demux function that adds bookmark and heading to page list
    """
    for flowable in doHeading(title, sty):
        page.append(flowable)


def doImage(Img, doc, titlename, sty):
    """
    Here we simplify the process of inserting an Image to the pdf story

    :param doc: an instance of autobasedoc

    #TODO make it more general, the doc.width is not reliable
    """
    if not Img is None:

        factor = doc.width / Img.drawWidth
        Img.drawHeight = Img.drawHeight * factor
        Img.drawWidth = Img.drawWidth * factor
        para = Paragraph(
            u"Fig. " + doc.figcounter() + u" " + titlename + u" Vertikal",
            sty.caption)

        return (Img, para)
    else:
        return ""


def PageNext(contents, nextTemplate):
    """
    switch to nextTemplate on next page
    """
    if isinstance(contents[-1], PageBreak):
        contents.insert(-1, nextTemplate)
    else:
        contents.append(nextTemplate)
        contents.append(PageBreak())
    return contents


###############################################################################

if __name__ == "__main__":

    print("this is a module")
    #print Paragraph styles added to the styles.stylesheet
    #print(styles.stylesheet.list() )

    #print(color_dict())
