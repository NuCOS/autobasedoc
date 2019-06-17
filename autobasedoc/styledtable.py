import random
import string
from reportlab.platypus import TableStyle, Table
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch, cm, mm
from autobasedoc import base_fonts, colors

def getTableStyle(tSty=None, tSpaceAfter=0, tSpaceBefore=0):
    """
    :param tSty: TableStyle(tSty) default is None
    :param tSpaceBefore: space before table, default: 0
    :param tSpaceAfter: space after table, default: 0

    :returns: TableStyle object

    use the add method of that object to add style commands e.g.:
    to add a background in the first row::

        tableStyle.add(("BACKGROUND",(0,0),(2,0),ar.colors.green))
        tableStyle.add(("BACKGROUND",(2,0),(4,0),ar.colors.lavender))

    to change text color on the first two columns::

        tableStyle.add(("TEXTCOLOR",(0,0),(1,-1),ar.colors.red))

    to change alignment of all cells to 'right'::

        tableStyle.add(("ALIGN",(0,0),(-1,-1),"RIGHT"))

    to add a grid for the whole table::

        tableStyle.add(("GRID",(0,0),(-1,-1),0.5,ar.colors.black))

    some further examples of command entries::

        ("ALIGN",(0,0),(1,-1),"LEFT"),
        ("ALIGN",(1,0),(2,-1),"RIGHT"),
        ("ALIGN",(-2,0),(-1,-1),"RIGHT"),
        ("GRID",(1,1),(-2,-2),1,ar.colors.green),
        ("BOX",(0,0),(1,-1),2,ar.colors.red),
        ("LINEABOVE",(1,2),(-2,2),1,ar.colors.blue),
        ("LINEBEFORE",(2,1),(2,-2),1,ar.colors.pink),
        ("BACKGROUND", (0, 0), (0, 1), ar.colors.pink),
        ("BACKGROUND", (1, 1), (1, 2), ar.colors.lavender),
        ("BACKGROUND", (2, 2), (2, 3), ar.colors.orange),
        ("BOX",(0,0),(-1,-1),2,ar.colors.black),
        ("GRID",(0,0),(-1,-1),0.5,ar.colors.black),
        ("VALIGN",(3,0),(3,0),"BOTTOM"),
        ("BACKGROUND",(3,0),(3,0),ar.colors.limegreen),
        ("BACKGROUND",(3,1),(3,1),ar.colors.khaki),
        ("ALIGN",(3,1),(3,1),"CENTER"),
        ("BACKGROUND",(3,2),(3,2),ar.colors.beige),
        ("ALIGN",(3,2),(3,2),"LEFT"),
        ("GRID", (0,0), (-1,-1), 0.25, ar.colors.black),
        ("ALIGN", (1,1), (-1,-1), "RIGHT")
        ("FONTSIZE", (1,0), (1,0), self.fontsizes["table"])

        ('SPAN',(1,0),(1,-1))
    """
    if not tSty:
        tSty = list()
    else:
        pass

    tableStyle = TableStyle(tSty)

    tableStyle.spaceAfter = tSpaceAfter
    tableStyle.spaceBefore = tSpaceBefore

    return tableStyle


class StyledTable(object):
    """
    data object to store all data and styles of ONE table

    This class is an independent representation for the metadata and parameters
    of the results to be shown in ONE table::

        +----------------------------------+
        |            table                 |
        |                                  |
        +----------------------------------+


    """

    def __init__(self, gridded=False, leftTablePadding=0, hTableAlignment=None):
        """
        :param gridded: if True, the table style is gridded, default is False
        :type gridded: bool
        :param leftTablePadding: if a number > 0 is inserted, the table gets a left empty column to be like left-padded
        :type leftTablePadding: int
        """
        self.hTableAlignment = hTableAlignment
        self.tableData = list()
        self.tableStyleCommands = list()
        # for finalizing specific cell formats
        self.tableExtraStyleCommands = list()
        self.fontsize = 10
        self.addTableStyleCommand(('FONT', (0, 0), (-1, -1),
                                   base_fonts()["normal"]))
        if gridded:
            self.addTableStyleCommand(("GRID", (0, 0), (-1, -1), 0.5,
                                       colors.black))
        if leftTablePadding:
            self.offsetCol = 1
            self.leftTablePadding = leftTablePadding
        else:
            self.offsetCol = 0
            self.leftTablePadding = 0
        self.headerRow = 0
        self.title = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(5))
        # BUG: VALIGN does not work with different font sizes !!!
        self.addTableStyleCommand(
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'))
        self.addTableStyleCommand(
            ('FONTSIZE', (0, 0), (-1, -1), self.fontsize))

    def setFontSizeColor(self, size, color, row, col):
        """
        FONTSIZE (or SIZE)      - takes fontsize in points; leading may get out of sync.
        TEXTCOLOR
        """
        cmd_size = ("FONTSIZE", (self.offsetCol + col, row),
                    (self.offsetCol + col, row), size)
        cmd_color = ("TEXTCOLOR", (self.offsetCol + col, row),
                     (self.offsetCol + col, row), color)

        # adjust the paddings in the cells with larger fonts
        cmd_padding_bottom = ('BOTTOMPADDING', (self.offsetCol + col, row),
                              (self.offsetCol + col, row), size - self.fontsize + 3)
        cmd_padding_top = ('TOPPADDING', (self.offsetCol + col, row),
                           (self.offsetCol + col, row), 0)
        cmd_padding_right = ('RIGHTPADDING', (self.offsetCol + col, row),
                             (self.offsetCol + col, row), 0.2 * cm)
        self.addTableExtraStyleCommand(cmd_size)
        self.addTableExtraStyleCommand(cmd_color)
        self.addTableExtraStyleCommand(cmd_padding_bottom)
        self.addTableExtraStyleCommand(cmd_padding_top)
        self.addTableExtraStyleCommand(cmd_padding_right)

    def addTableExtraStyleCommand(self, cmd):
        if isinstance(cmd, list):
            for cm in cmd:
                self.tableExtraStyleCommands.append(cm)

        if isinstance(cmd, tuple):
            self.tableExtraStyleCommands.append(cmd)

    def addTableStyleCommand(self, cmd, extra=False):
        """
        Adds style command to table.

        line commands are like:
        op, start, stop, weight, colour, cap, dashes, join, linecount, linespacing

        op is one of:
        GRID, BOX,OUTLINE, INNERGRID, LINEBELOW, LINEABOVE, LINEBEFORE, LINEAFTER

        cell commands are like ...

        :param cmd: one table command data for styles
        :type cmd: tuple
        """
        if isinstance(cmd, list):
            for cm in cmd:
                self.tableStyleCommands.append(cm)
        if isinstance(cmd, tuple):
            self.tableStyleCommands.append(cmd)

    def setTableData(self, data):
        """
        Overwrites the table data with fresh new data.
        If leftTablePadding is activated an empty column is inserted here automatically.

        :param data: the new data
        :type data: list of tuples

        """
        self.tableData = data
        if self.leftTablePadding > 0:
            for t in self.tableData:
                t.insert(0, "")

    def addTableLine(self, line):
        """
        Adds a table line to data.
        If leftTablePadding is activated an empty column is inserted here automatically.

        :param line: the data of one table line
        :type line: tuple, list
        """
        if isinstance(line, tuple):
            line = list(line)
        if self.leftTablePadding > 0:
            line.insert(0, "")
        self.tableData.append(line)

    def addHorizontalLines(self, color="blue", offsetCol=None, exclude=[]):
        """
        Adds horizontal lines only. Apply after inserting all data and after inserting the header line.
        If no header line exists also a top line is included.

        :param color: the color of the horizontal line
        :type color: str
        """
        if offsetCol is None:
            offsetCol = self.offsetCol
        color = getattr(colors, color)
        for ri in range(self.headerRow, self.linesCount()):
            if ri in exclude:
                continue
            self.addTableStyleCommand(
                ("LINEBELOW", (offsetCol, ri), (-1, ri), 0.4, color))
        if self.headerRow == 0:
            self.addTableStyleCommand(
                ("LINEABOVE", (offsetCol, 0), (-1, 0), 0.4, color))

    def addDoubleLine(self, color="blue", line=0):
        """
        Adds a double line below the line specified

        :param line: the number of the line below which the double line is inserted
        :type col: int
        :param color: the color of the vertical line
        :type color: str
        """
        cmd = ("LINEBELOW", (self.offsetCol, line), (-1, line), 0.4,
               color, 1, None, None, 2, 0.6)
        self.tableStyleCommands.append(cmd)

    def addVerticalLine(self, col, color="blue"):
        """
        Adds vertical lines only. Apply after inserting all data.

        :param col: the number of the column after which the vertical line is inserted
        :type col: int
        :param color: the color of the horizontal line
        :type color: str
        """
        color = getattr(colors, color)
        self.addTableStyleCommand(
            ("LINEAFTER", (col + self.offsetCol, 0), (col + self.offsetCol, -1), 0.4, color))

    def addTableHeader(self, line, fonttype="bold", color="blue"):
        """
        Prepends a table line to data and insert the correct styles, like double underline and bold.

        :param line: the data for the header line
        :type line: tuple, list
        :param fonttype: one of normal, bold, italic
        :type fonttype: str
        :param color: the color of the horizontal line
        :type color: str
        """
        self.headerRow = 1
        color = getattr(colors, color)
        line = copy.copy(line)
        if isinstance(line, tuple):
            line = list(line)
        if self.leftTablePadding > 0:
            line.insert(0, "")
        self.tableData.insert(0, line)
        cmd = ('FONT', (self.offsetCol, 0),
               (-1, 0), _baseFontNames[fonttype])
        self.tableStyleCommands.append(cmd)
        self.addDoubleLine()

    def linesCount(self):
        """
        Returns the number of rows/lines including header line.

        """
        return len(self.tableData)

    def colsCount(self):
        """
        Returns the number of columns.

        """
        return len(self.tableData[0])

    def handleStyleCommands(self):
        """
        Creates real tableStyle from tableStyleCommands.

        """
        tableStyle = getTableStyle()
        for cmd in self.tableStyleCommands:
            if not len(cmd) == 0:
                tableStyle.add(*cmd)
        for cmd in self.tableExtraStyleCommands:
            if not len(cmd) == 0:
                tableStyle.add(*cmd)
        return tableStyle

    @property
    def as_flowable(self):
        """
        Shortage name
        """
        if not self.tableData:
            self.tableData = [[""]]
        return self.layoutTable(hTableAlignment=None, colWidths=None)

    def layoutTable(self, hTableAlignment=TA_LEFT, colWidths=None):
        """
        Returns a table flowable with automatically estimated column width.

        :param styledTable: a styled table
        :type styledTable: StyledTable
        :param hTableAlignment: the table alignment on the frame
        :type hTableAlignment: int
        :param colWidths: the columns width in cm
        :type colWidths: list
        :param spaceBefore: the space above the table in cm
        :type spaceBefore: float
        :param spaceAfter: the space below the table in cm
        :type spaceAfter: float

        :returns: a table flowable element
        """
        self.addTableStyleCommand(
            ('LEFTPADDING', (0, 0), (-1, -1), 0.1 * cm))
        self.addTableStyleCommand(
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'))
        if colWidths:
            colWidths = [x * cm for x in colWidths]
        table = Table(self.tableData, colWidths=colWidths,
                         spaceBefore=0, spaceAfter=0)
        table.setStyle(self.handleStyleCommands())
        if hTableAlignment:
            table.hAlign = hTableAlignment
        elif self.hTableAlignment:
            table.hAlign = self.hTableAlignment
        return table
