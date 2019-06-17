
def addPlugin(canv, doc, frame="First"):
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

    def drawString(pitem, text, posy):
        """
        draws a String in posy:

        - l draws in align 'Left'
        - c draws in align 'Center'
        - r draws in align 'Right'

        """
        if pitem.pos == "l":
            canv.drawString(doc.leftMargin, posy, text)

        elif pitem.pos == "c":
            canv.drawCentredString(doc.centerM, posy, text)

        elif pitem.pos == "r":
            canv.drawRightString(doc.rightM, posy, text)

    def drawLine(pitem, posy):  #,rightMargin=None
        """
        draws a Line in posy::

            l---------------r
        """
        left, right = doc.leftM, doc.rightM

        #print("drawLine at posy:",posy)
        #print("from %s to %s"%(left,right))

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
                x = doc.rightM
                x -= pitem.image.drawWidth
                y -= pitem.image.drawHeight
                x, y = shift(pitem, x, y)

            if pitem.pos.startswith("l"):
                x = doc.leftM
                #x-=pitem.image.drawWidth
                y -= pitem.image.drawHeight
                x, y = shift(pitem, x, y)
            else:
                x, y = shift(pitem, x, y)

        elif pitem.typ.startswith("footer"):
            if pitem.pos.startswith("r"):
                x = doc.rightM
                x -= pitem.image.drawWidth
                y -= pitem.image.drawHeight
                x, y = shift(pitem, x, y)

            if pitem.pos.startswith("l"):
                x = doc.leftM
                #x-=pitem.image.drawWidth
                y -= pitem.image.drawHeight
                x, y = shift(pitem, x, y)
            else:
                x, y = shift(pitem, x, y)

        pitem.image.drawOn(canv, x, y)
        #print("added image")

    lkeys = []

    if doc.pageInfos:

        for pkey, pitem in doc.pageInfos.items():
            #print(pkey)
            #pitem=doc.pageInfos[pkey]
            #print( pitem.frame )

            if pitem.frame.startswith(frame):
                lkeys.append(pkey)

                text = "%s" % pitem.text
                #add Page Number if requested
                if pitem.addPageNumber:
                    text += "%d" % doc.page
                    #if is_talkative:
                    print(text)
                if pitem.typ.startswith("header"):
                    #Header
                    posy = doc.headM
                    if not pitem.text is None:
                        #print("drawString",text)
                        drawString(pitem, text, posy)
                    elif not pitem.image is None:
                        pos = (doc.leftMargin, posy)
                        drawImage(pitem, pos)
                        #print("drawImage",pitem.image)
                    if pitem.line:
                        canv.setLineWidth(doc.lineWidth)
                        drawLine(pitem, posy - doc.topM + doc.fontSize)

                elif pitem.typ.startswith("footer"):
                    #Footer
                    posy = doc.bottomM
                    if not pitem.text is None:
                        drawString(pitem, text, posy)
                    elif not pitem.image is None:
                        pos = (doc.leftMargin, posy)
                        drawImage(pitem, pos)
                        #print("drawImage",pitem.image)
                    if pitem.line:
                        canv.setLineWidth(doc.lineWidth)
                        drawLine(pitem, posy + doc.topM)
                else:
                    break
        if len(lkeys) == 0:
            addPlugin(canv, doc, frame="First")
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
                 rightMargin=None, shift=None):
        self.typ = typ
        self.pos = pos
        self.text = text
        self.image = image
        self.line = line
        self.frame = frame
        self.addPageNumber = addPageNumber
        if rightMargin is not None:
            setattr(self, "rightMargin", rightMargin)
        if shift is not None:
            setattr(self, "shift", shift)
