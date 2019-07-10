"""
tableofcontents
===============

.. module:: tableofcontents
   :platform: Unix, Windows
   :synopsis: a tableofcontents that breaks not to the next frame but to the next page

.. moduleauthor:: Johannes Eckstein

"""
from reportlab import rl_config
from reportlab.platypus import Table, Paragraph, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents, drawPageNumbers

class AutoTableOfContents(TableOfContents):

    def __init__(self):
        super(AutoTableOfContents, self).__init__()

    def wrap(self, availWidth, availHeight):
        "All table properties should be known by now."

        # makes an internal table which does all the work.
        # we draw the LAST RUN's entries!  If there are
        # none, we make some dummy data to keep the table
        # from complaining
        if len(self._lastEntries) == 0:
            _tempEntries = [(0,'Placeholder for table of contents',0,None)]
        else:
            _tempEntries = self._lastEntries

        def drawTOCEntryEnd(canvas, kind, label):
            '''Callback to draw dots and page numbers after each entry.'''
            label = label.split(',')
            page, level, key = int(label[0]), int(label[1]), eval(label[2],{})
            style = self.getLevelStyle(level)
            if self.dotsMinLevel >= 0 and level >= self.dotsMinLevel:
                dot = ' . '
            else:
                dot = ''
            if self.formatter: page = self.formatter(page)
            drawPageNumbers(canvas, style, [(page, key)], availWidth, availHeight, dot)
        self.canv.drawTOCEntryEnd = drawTOCEntryEnd

        tableData = []
        for (level, text, pageNum, key) in _tempEntries:
            style = self.getLevelStyle(level)
            if key:
                text = '<a href="#%s">%s</a>' % (key, text)
                keyVal = repr(key).replace(',','\\x2c').replace('"','\\x2c')
            else:
                keyVal = None
            para = Paragraph('%s<onDraw name="drawTOCEntryEnd" label="%d,%d,%s"/>' % (text, pageNum, level, keyVal), style)
            if style.spaceBefore:
                tableData.append([Spacer(1, style.spaceBefore),])
            tableData.append([para,])

        self._table = TocTable(tableData, colWidths=(availWidth,), style=self.tableStyle)

        self.width, self.height = self._table.wrapOn(self.canv, availWidth, availHeight)
        return (self.width, self.height)


class TocTable(Table):

    def __init__(self, data, **kwargs):
        super(TocTable, self).__init__(data, **kwargs)

    def split(self, availWidth, availHeight):
        self._calc(availWidth, availHeight)
        if self.splitByRow:
            if not rl_config.allowTableBoundsErrors and self._width>availWidth: return []
            return [self._splitRows(availHeight)[0], PageBreak(), self._splitRows(availHeight)[-1]]
        else:
            raise NotImplementedError
