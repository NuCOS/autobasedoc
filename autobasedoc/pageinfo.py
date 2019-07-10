"""
pageinfo
========

.. module:: pageinfo
   :platform: Unix, Windows
   :synopsis: place header and footer

.. moduleauthor:: Johannes Eckstein

"""

def addPlugin(canv, doc, frame=None, talkative=False):
    """
    holds all functions to handle placing all elements on the canvas...

    :param canv: canvas object
    :param doc: AutoDocTemplate instance
    :param frame: template name of the Frame

    This function suggests that you have stored page info Items
    in doc.pageInfos.

    By default if there is no frame='Later' option, we use the frame='First'

    If you don't want to decorate your Later pages,
    please define an empty pageTemplate with frame='Later'

    """
    _left_margin = False
    _right_margin = False
    _top_margin = False
    _bottom_margin = False

    #centerM
    def center_margin():
        if (_left_margin or _right_margin) and doc.leftMargin and doc.rightMargin and frame is not None:
            return (frame._width - (doc.leftMargin + doc.rightMargin)) / 2.
        if frame is not None:
            return (frame._width - (frame._leftPadding + frame._rightPadding)) / 2.
        return doc.pagesize[0]/2.

    #leftM
    def left_margin():
        if _left_margin and doc.leftMargin:
            return doc.leftMargin
        if frame is not None:
            return frame._leftPadding
        return 0.

    #rightM
    def right_margin():
        if _right_margin and doc.rightMargin:
            return frame._width - doc.rightMargin
        if frame is not None:
            return frame._width - frame._rightPadding
        return doc.pagesize[0]

    #headM
    def head_margin():
        if _top_margin and doc.topMargin:
            return frame._height - (doc.topMargin + doc.topM)
        if frame is not None:
            return frame._height - (frame._topPadding + doc.topM)
        return doc.pagesize[1]

    #bottomM
    def bottom_margin():
        if _bottom_margin and doc.bottomMargin:
            return doc.bottomMargin + doc.bottomM
        if frame is not None:
            return frame._bottomPadding + doc.bottomM
        return 0.

    def drawString(pitem, text, posy):
        """
        draws a String in posy:

        - l draws in align 'Left'
        - c draws in align 'Center'
        - r draws in align 'Right'

        """
        if pitem.pos == "l":
            canv.drawString(left_margin(), posy, text)

        elif pitem.pos == "c":
            canv.drawCentredString(center_margin(), posy, text)

        elif pitem.pos == "r":
            canv.drawRightString(right_margin(), posy, text)

    def drawLine(pitem, posy):
        """
        draws a Line in posy::

            l---------------r
        """
        left, right = left_margin(), right_margin()

        if getattr(pitem, "rightMargin", None):
            right -= pitem.rightMargin

        canv.line(left, posy, right, posy)

    def drawImage(pitem, pos):
        """
        pos = (x,y)

        draws a footer/header image at pos if pitem.pos='r'::

                +-------------------+ pos
                |                   |
                |       image       |
                |                   |
                |                   |
                +-------------------+

        draws a footer/header image at pos if pitem.pos='l'::

            pos +-------------------+
                |                   |
                |       image       |
                |                   |
                |                   |
                +-------------------+

        every image can be shifted/translated if a 'shift' attribute is found on pitem::

                ^
                |y
            pos +-->
                 x
        """

        def shift(pitem, x, y):
            """
            apply shift x,y on pitem
            """
            if getattr(pitem, "shift", None):
                x += pitem.shift[0]
                y += pitem.shift[1]

            return x, y

        x, y = pos

        ### here must be placed a positioning for the three locations
        if pitem.typ.startswith("header"):
            if pitem.pos.startswith("r"):
                x = right_margin()
                x -= pitem.image.drawWidth
                y -= pitem.image.drawHeight

            if pitem.pos.startswith("l"):
                x = left_margin()
                #x-=pitem.image.drawWidth
                y -= pitem.image.drawHeight
            #finally
            x, y = shift(pitem, x, y)

        elif pitem.typ.startswith("footer"):
            if pitem.pos.startswith("r"):
                x = right_margin()
                x -= pitem.image.drawWidth
                y -= pitem.image.drawHeight

            if pitem.pos.startswith("l"):
                x = left_margin()
                #x-=pitem.image.drawWidth
                y -= pitem.image.drawHeight
            #finally
            x, y = shift(pitem, x, y)

        pitem.image.drawOn(canv, x, y)
        #print("added image")

    lkeys = []

    if doc.pageInfos:
        if frame is None:
            return

        for pkey, pitem in doc.pageInfos.items():
            if talkative:
                print(pkey)
            #pitem=doc.pageInfos[pkey]

            if getattr(pitem, "rightMargin", None) is not None:
                _right_margin = getattr(pitem, "rightMargin")
            if getattr(pitem, "leftMargin", None) is not None:
                _left_margin = getattr(pitem, "leftMargin")
            if getattr(pitem, "topMargin", None) is not None:
                _top_margin = getattr(pitem, "topMargin")
            if getattr(pitem, "bottomMargin", None) is not None:
                _bottom_margin = getattr(pitem, "bottomMargin")

            if frame.id.startswith(pitem.frame):
                lkeys.append(pkey)

                text = "%s" % pitem.text
                #add Page Number if requested
                if pitem.addPageNumber:
                    if doc.page:
                        text += "%d" % doc.page
                    if talkative:
                        print(text)

                if pitem.typ.startswith("header"):
                    #print(text)
                    #Header
                    posy = head_margin()
                    if pitem.text is not None:
                        #print("drawString",text)
                        drawString(pitem, text, posy)
                    elif pitem.image is not None:
                        pos = (doc.leftMargin, posy)
                        drawImage(pitem, pos)
                        #print("drawImage",pitem.image)
                    if pitem.line:
                        canv.setLineWidth(doc.lineWidth)
                        drawLine(pitem, posy - doc.topM + doc.fontSize)

                elif pitem.typ.startswith("footer"):
                    #Footer
                    posy = bottom_margin()
                    if pitem.text is not None:
                        drawString(pitem, text, posy)
                    elif pitem.image is not None:
                        pos = (doc.leftMargin, posy)
                        drawImage(pitem, pos)
                        #print("drawImage",pitem.image)
                    if pitem.line:
                        canv.setLineWidth(doc.lineWidth)
                        drawLine(pitem, posy + doc.topM)
                else:
                    break

        if len(lkeys) == 0:
            addPlugin(canv, doc, frame=None)
    else:
        pass
        #print("going through the pageInfo items:",lkeys)

class PageInfo(object):
    """
    a Class to handle header and footer elements, that raster into a frame::

        l    c    r

    :param typ: header/footer
    :param pos: 'l'/'c'/'r'
    :param text: text of header or footer element
    :param image: image preferrably as pdf Image
    :param addPageNumber: True/False

    As of now we consider either text or image, and will not handle these cases separately.

    """

    def __init__(self, typ, pos, text, image, line, frame, addPageNumber,
                 rightMargin=None, leftMargin=None,
                 topMargin=None, bottomMargin=None,
                 shift=None):

        self.typ = typ
        self.pos = pos
        self.text = text
        self.image = image
        self.line = line
        self.frame = frame
        self.addPageNumber = addPageNumber

        if rightMargin is not None:
            setattr(self, "rightMargin", rightMargin)
        if leftMargin is not None:
            setattr(self, "leftMargin", leftMargin)
        if topMargin is not None:
            setattr(self, "topMargin", topMargin)
        if bottomMargin is not None:
            setattr(self, "bottomMargin", bottomMargin)
        if shift is not None:
            setattr(self, "shift", shift)
