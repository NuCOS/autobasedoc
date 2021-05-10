from copy import deepcopy, copy
import autobasedoc.autorpt as ar

from footer import Footer
from header import Header


class EmptyFlowable():
    @property
    def as_flowable(self):
        return ar.Spacer(width=2.0 * ar.cm, height=0.01 * ar.cm)


def drawFirstPage(canv, doc):
    """
    This is the Title Page Template (Landscape Oriented)
    """
    canv.saveState()
    frame, pagesize = doc.getFrame(doc.template_id)
    canv.setPageSize(pagesize)
    canv.setFont(ar.base_fonts()["normal"], doc.fontSize)
    canv.restoreState()

def drawLaterPage(canv, doc):
    """
    This is the Template of any later drawn Protrait Oriented Page
    """
    canv.saveState()
    frame, pagesize = doc.getFrame(doc.template_id)
    canv.setPageSize(pagesize)
    canv.setFont(ar.base_fonts()["normal"], doc.fontSize)
    canv.restoreState()

def drawLaterSpecialPage(canv, doc):
    """
    This is the Template of any later drawn Protrait Oriented Page ?? not known
    """
    canv.saveState()
    frame, pagesize = doc.getFrame(doc.template_id)
    canv.setPageSize(pagesize)
    canv.setFont(ar.base_fonts()["normal"], doc.fontSize)
    canv.restoreState()

def drawFirstLandscape(canv, doc):
    """
    This is the Title Page Template (Landscape Oriented)
    """
    canv.saveState()
    frame, pagesize = doc.getFrame(doc.template_id)
    canv.setPageSize(pagesize)
    canv.setFont(ar.base_fonts()["normal"], doc.fontSize)
    canv.restoreState()

def drawLaterLandscape(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()
    frame, pagesize = doc.getFrame(doc.template_id)
    canv.setPageSize(pagesize)
    canv.setFont(ar.base_fonts()["normal"], doc.fontSize)
    canv.restoreState()

def drawLaterSpecialLandscape(canv, doc):
    """
    This is the Template of any later drawn Landscape Oriented Page
    """
    canv.saveState()
    frame, pagesize = doc.getFrame(doc.template_id)
    canv.setPageSize(pagesize)
    canv.setFont(ar.base_fonts()["normal"], doc.fontSize)
    canv.restoreState()


class Document(list):
    """
    holds the pages as a list structure, where key is the identifier of the page
    and the value is a dict consisting of flowables-lists for each page (like table, paragraph, figure)

    footer and header are also flowables

    """

    def __init__(self, orientation="landscape", filename=None, debug=False):
        
        self.laterFrames = {"portrait": "LaterPage", "landscape": "LaterLandscape"}
        self.orientation = orientation
        if orientation == "portrait":
            self.refs = [drawFirstPage, drawLaterPage, drawLaterSpecialPage]
            self.frames = [1,1,1]
        elif orientation == "landscape":
            self.refs = [drawFirstLandscape, drawLaterLandscape, drawLaterSpecialLandscape]
            self.frames = [1,2,1]
        self.filename = filename
        self.header = Header()
        self.footer = Footer()
        self.debug = debug
        self.doc = None

    @property
    def cln(self):
        return self._cln()

    @classmethod
    def _cln(cls):
        return cls.__name__

    def insert_page(self, n, bookmark=None, header=None, footer=None, framestyle="single", content={}, pagenumber=None):
        if header is None:
            header = self.header
        if footer is None:
            footer = self.footer
        if header == "empty":
            header = Header()
        if footer == "empty":
            footer = Footer()
        if "top" not in content:
            content.update({"top": EmptyFlowable().as_flowable})
        if "bottom" not in content:
            content.update({"bottom": EmptyFlowable().as_flowable})
        if framestyle == "double":
            if "left" not in content:
                content.update({"left": [EmptyFlowable().as_flowable]})
            if "right" not in content:
                content.update({"right": [EmptyFlowable().as_flowable]})
        if framestyle == "single":
            if "center" not in content:
                content.update({"center": [EmptyFlowable().as_flowable]})
        page = {
            "content": content,
            "header": header,
            "footer": footer,
            "pagenumber": pagenumber,
            "framestyle": framestyle,
            "bookmark": bookmark
        }
        self.insert(n, page)


    def add_page(self, bookmark=None, header=None, footer=None, framestyle="single", content={}, pagenumber=None):
        """
        adds a page to the document, keeping the order

        example "double" framestyle:

        - content = {"left": [figure1, table1], "right": [figure2, table2], "top": [paragraph], "bottom": [table]}

         ____________________________________________________
        | header-left      header-center      header-right   |
        |                                                    |
        |  -----------------------top----------------------  |
        |     ______________              ______________     |
        |    |              |            |              |    |
        |    |     left     |            |     right    |    |
        |    |              |            |              |    |
        |    |______________|            |______________|    |
        |                                                    |
        |  ----------------------bottom--------------------  |
        |                                                    |
        | footer-left       footer-center     footer-right   |
        |______________________________________page-number___|


        example "single" framestyle:

        - content = {"center": [figure, table], "top": [table1], "bottom": [table2]}

         ____________________________________________________
        | header-left      header-center      header-right   |
        |                                                    |
        |  -----------------------top----------------------  |
        |     __________________________________________     |
        |    |                                          |    |
        |    |                   center                 |    |
        |    |                                          |    |
        |    |__________________________________________|    |
        |                                                    |
        |  ----------------------bottom--------------------  |
        |                                                    |
        | footer-left       footer-center     footer-right   |
        |______________________________________page-number___|

        - must-work: a single page switches frame structure from single to double and back

        - frame structure may be infered from content structure, so maybe it is not a parameter???

        - if header/footer must be empty on that page there should be "empty" in

        - pagenumber="right"/"center"/"left" adds a standard number on that page below the footer?

        """
        # most easiest implementation,
        # use deepcopy to make it independent from changes later on
        if header is None:
            header = self.header
        if footer is None:
            footer = self.footer
        if header == "empty":
            header = Header()
        if footer == "empty":
            footer = Footer()
        if "top" not in content:
            content.update({"top": EmptyFlowable().as_flowable})
        if "bottom" not in content:
            content.update({"bottom": EmptyFlowable().as_flowable})
        if framestyle == "double":
            if "left" not in content:
                content.update({"left": [EmptyFlowable().as_flowable]})
            if "right" not in content:
                content.update({"right": [EmptyFlowable().as_flowable]})
        if framestyle == "single":
            if "center" not in content:
                content.update({"center": [EmptyFlowable().as_flowable]})
        page = {
            "content": content,
            "header": header,
            "footer": footer,
            "pagenumber": pagenumber,
            "framestyle": framestyle,
            "bookmark": bookmark
        }
        self.append(page)

    def add_header(self, header):
        """
        adds a default header which is displayed if no header is specified on page
        no header is shown on the page if "empty" is on the page

        header and footer are usually structured as follows: a table of tables
        (the inner tables are e.g. mini-tables [figure|label] or three-row-tables)

        table:
         ___________________________________________________
        | table                 table                 table |
        |___________________________________________________|

        headers are added as styledTables
        """
        self.header = header

    def add_footer(self, footer):
        """
        adds a default footer which is displayed if no header is specified on page
        no footer is shown on the page if "empty" is on the page

        footers are added as styledTables
        """
        self.footer = footer

    def add_chapter_bookmark(self, bookmark):
        self.append({"chapter-bookmark": bookmark})


    def setDocument(self,
                    version="2.0.0",
                    leftMargin=0.9,
                    rightMargin=0.9,
                    topMargin=0.9,
                    bottomMargin=0.9,
                    producer="LDM-Tool",
                    title=None,
                    author=None,
                    subject=None,
                    creator="Daimler",
                    keywords=[]):
        """
        :param leftMargin: Linke Randdicke in [cm]
        :param rightMargin: Rechte Randdicke in [cm]
        :param topMargin: Obere Randdicke in [cm]
        :param bottomMargin: Untere Randdicke in [cm]
        """
        self.doc = ar.AutoDocTemplate(
            self.filename,
            onFirstPage=(self.refs[0], self.frames[0]),
            onLaterPages=(self.refs[1], self.frames[1]),
            onLaterSPages=(self.refs[2], self.frames[2]),
            leftMargin=leftMargin * ar.cm,
            rightMargin=rightMargin * ar.cm,
            topMargin=topMargin * ar.cm,
            bottomMargin=bottomMargin * ar.cm,
            title=title,
            producer="%s %s" % (producer, version),
            author=author,
            subject=subject,
            creator=creator,
            keywords=keywords,
            debug=self.debug)

    def ensure_flowables(self, frameInfo, content, fullPage):
        """
        """
        nextPage = None
        content_out = []
        availableHeight = frameInfo._aH
        for i, element in enumerate(content):
            if hasattr(element, "as_flowable"):
                if element.getTableHeight(frameInfo) > availableHeight:
                    # n = int(element.getTableHeight(frameInfo)/frameInfo._aH) + 1
                    tables = element.split_table_iterative(frameInfo, availableHeight)
                    nextPage = deepcopy(fullPage)
                    content_out.append(tables[0].as_flowable)
                    # NOTE asume here only single frame pages
                    nextPage["content"]["center"][i] = tables[1]
                else:
                    content_out.append(element.as_flowable)
            else:
                content_out.append(element)
                height = element.wrap(frameInfo._aW, frameInfo._aH)[1]
                availableHeight -= height
        return content_out, nextPage

    def create_pdf(self, title, author, producer, version, filename=None):
        """
        starts the creation of the pdf and saves in filename (includes path)

        returns filename
        """
        if filename:
            self.filename = filename
        if self.doc is None:
            self.setDocument(title=title, author=author, producer=producer, version=version)
        content = []
        pageState = "single"
        chapter = None
        for i, page in enumerate(copy(self)):
            content, chapter, pageState = self._apply_page(page, content, chapter, pageState)
        # 
        # 
        # print("----------\n\n\n", content)
        self.doc.multiBuild(content)
        print("save pages %s" % self.filename)
        return self.filename


    def _apply_page(self, page, content, chapter, pageState, deep=False):
        """ 
        not used from outside, only internal use!
        """
        if "chapter-bookmark" in page:
            chapter = page["chapter-bookmark"]
            return content, chapter, pageState
        if page["framestyle"] == "double":
            if chapter:
                content.append(chapter)
            frameInfo, _ = self.doc.getFrame(self.laterFrames[self.orientation])
            # NOTE how to make sure next page is a double page ??
            content.extend(page["content"]["left"])
            content.append(ar.FrameBreak())
            content.extend(page["content"]["right"])
            content.append(ar.FrameBreak())
            #content.append(page["content"]["top"])
            #content.append(page["content"]["bottom"])

            # frameWidth = frameInfo._aW - (frameInfo._x1 * 2.)
            # print("frameWidth:", frameWidth)
            marginSide = self.doc.leftMargin + self.doc.rightMargin
            content.append(page["bookmark"])
            content.append(page["header"].margin_top)
            content.append(page["header"].layoutFullWidthTable(
                frameInfo, marginSide=marginSide
            ))
            headerHeight = page["header"].height(frameInfo)
            content.append(page["footer"].margin_top(frameInfo, headerHeight))
            content.append(page["footer"].layoutFullWidthTable(
                frameInfo, marginSide=marginSide, ratios=[0.3, 0.2, 0.2, 0.3]
            ))
            content.append(ar.PageBreak())
            pageState = "double"
            nextPage = None
        elif page["framestyle"] == "single":
            if pageState=="double" or pageState=="later":
                # content.append(self.doc.getSpecialTemplate())
                # was LaterSL
                content = ar.PageNext(content, self.doc.getSpecialTemplate(temp_name="Later"))
                frameInfo, _ = self.doc.getFrame(self.laterFrames[self.orientation], last=True)
            else:
                frameInfo, _ = self.doc.getFrame(self.laterFrames[self.orientation])
            if chapter:
                content.append(chapter)
            content.append(page["content"]["top"])
            # NOTE the possibility of tables flowing onto next page
            # is only provided on single pages
            flowable, nextPage = self.ensure_flowables(frameInfo, page["content"]["center"], page)
            content.extend(flowable)
            content.append(page["content"]["bottom"])
            content.append(ar.FrameBreak())
            if not deep:
                content.append(page["bookmark"])
            marginSide = self.doc.leftMargin + self.doc.rightMargin
            content.append(page["header"].margin_top)
            content.append(page["header"].layoutFullWidthTable(
                frameInfo, marginSide=marginSide
            ))
            headerHeight = page["header"].height(frameInfo)
            content.append(page["footer"].margin_top(frameInfo, headerHeight))
            content.append(page["footer"].layoutFullWidthTable(
                frameInfo, marginSide=marginSide, ratios=[0.3, 0.2, 0.2, 0.3]
            ))
            content.append(ar.PageBreak())
            pageState = "later"
        else:
            print("unknown frame style")
            raise Exception
        if nextPage:
            content, chapter, pageState = self._apply_page(nextPage, content, chapter, pageState, deep=True)
        return content, None, pageState
