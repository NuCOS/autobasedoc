"""
Images as Flowables

Pdf and Svg Images can be embedded from file, 
matplotlib drawings can be embedded as file-like objects
and behave like a Flowable.

SVG images can currently only be returned as a Drawing:

from reportlab.graphics.shapes import Drawing

reportlab.lib.utils.ImageReader

"""

from reportlab.platypus import Image, Flowable
from reportlab.lib.units import inch,cm,mm

from pdfrw import PdfReader,PdfDict #,PdfFileWriter
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT

from svglib.svglib import svg2rlg

def form_xo_reader(imgdata):
    page, = PdfReader(imgdata).pages
    return pagexobj(page)

def getSvg(path):
    """
    return reportlab.graphics.shapes.Drawing() object 
    with the contents of the SVG specified by path
    """
    return svg2rlg(path)

def scaleDrawing(drawing,factor,showBoundary=False):
    """
    scale a reportlab.graphics.shapes.Drawing() object, 
    leaving its aspect ratio unchanged
    """
    sx=sy=factor
    drawing.width,drawing.height = drawing.minWidth()*sx, drawing.height*sy
    drawing.scale(sx,sy)
    if showBoundary:
        drawing._showBoundary = True
    
    return drawing
    
def getScaledSvg(path,factor):
    """
    get a scaled svg image from file
    """
    drawing = getSvg(path)
    
    return scaleDrawing(drawing,factor)
    
class PdfImage(Flowable):
    """
    PdfImage wraps the first page from a PDF file as a Flowable
    which can be included into a ReportLab Platypus document.
    Based on the vectorpdf extension in rst2pdf (http://code.google.com/p/rst2pdf/)

    This can be used from the place where you want to return your matplotlib image
    as a Flowable:
        
        img = BytesIO()
        
        fig, ax = plt.subplots(figsize=(canvaswidth,canvaswidth))
        
        ax.plot([1,2,3],[6,5,4],antialiased=True,linewidth=2,color='red',label='a curve')
        
        fig.savefig(img,format='PDF')
        
        return(PdfImage(img))
        
    """

    def __init__(self, filename_or_object, width=None, height=None, kind='direct'):
        # If using StringIO buffer, set pointer to begining
        if hasattr(filename_or_object, 'read'):
            filename_or_object.seek(0)
            #print("read")
        self.page = PdfReader(filename_or_object, decompress=False).pages[0]
        self.xobj = pagexobj(self.page)

        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth)/self.imageHeight
        if kind in ['direct','absolute'] or width==None or height==None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound','proportional']:
            factor = min(float(width)/self._w,float(height)/self._h)
            self.drawWidth = self._w*factor
            self.drawHeight = self._h*factor

    def wrap(self, availableWidth, availableHeight):
        """
        returns draw- width and height

        convenience function to adapt your image 
        to the available Space that is available
        """
        return self.drawWidth, self.drawHeight

    def drawOn(self, canv, x, y, _sW=0):
        """
        translates Bounding Box and scales the given canvas
        """
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        #xobj_name = makerl(canv._doc, self.xobj)
        xobj_name = makerl(canv, self.xobj)

        xscale = self.drawWidth/self._w
        yscale = self.drawHeight/self._h

        x -= self.xobj.BBox[0] * xscale
        y -= self.xobj.BBox[1] * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()
        
class PdfAsset(Flowable):
    """
    read in the first page of a PDF file from file
    
    it can e used like a reportlab.platypus.Flowable()
    """
    def __init__(self,fname,width=None,height=None,kind='direct'):

        self.page = PdfReader(fname=fname, decompress=False).pages[0]
        self.xobj = pagexobj(self.page)

        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth)/self.imageHeight
        if kind in ['direct','absolute'] or width==None or height==None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound','proportional']:
            factor = min(float(width)/self._w,float(height)/self._h)
            self.drawWidth = self._w*factor
            self.drawHeight = self._h*factor

    def wrap(self, width, height):
        return self.imageWidth, self.imageHeight

    def drawOn(self, canv, x, y, _sW=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))
        canv.saveState()
        img = self.xobj
        if isinstance(img, PdfDict):
            xscale = self.imageWidth / img.BBox[2]
            yscale = self.imageHeight / img.BBox[3]
            canv.translate(x, y)
            canv.scale(xscale, yscale)
            canv.doForm(makerl(canv, img))
        else:
            #canv.drawInlineImage(img, x, y-self.imageHeight, self.imageWidth, self.imageHeight)
            canv.drawImage(img, x, y, self.imageWidth, self.imageHeight)
        canv.restoreState()