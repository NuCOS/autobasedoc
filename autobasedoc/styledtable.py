"""
styledtable
===========

.. module:: styledtable
   :platform: Unix, Windows
   :synopsis: a layouted table

.. moduleauthor:: Oliver Braun
"""
import random
import string
import copy
from reportlab.platypus import TableStyle, Table, Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch, cm, mm
from autobasedoc import base_fonts, colors
from collections import OrderedDict, defaultdict
from autobasedoc.fonts import getFont

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

    def __init__(self, gridded=False, leftTablePadding=0, hTableAlignment=None, colWidths=None):
        """
        :param gridded: if True, the table style is gridded, default is False
        :type gridded: bool
        :param leftTablePadding: if a number > 0 is inserted, the table gets a left empty column to be like left-padded
        :type leftTablePadding: int
        """
        self.hTableAlignment = hTableAlignment or TA_CENTER
        self.colWidths = colWidths
        self.rightPadding = 0
        self.spaceBefore = 0
        self.spaceAfter = 0
        self.tableData = list()
        self.tableStyleCommands = list()
        # for finalizing specific cell formats
        self.tableExtraStyleCommands = list()
        self.fontsize = 10
        self.font = getFont(base_fonts()["normal"])
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
               (-1, 0), base_fonts()[fonttype])
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
        return self.layoutTable()

    def layoutTable(self, hTableAlignment=None, colWidths=None):
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
        if hTableAlignment is not None:
            table.hAlign = hTableAlignment
        else:
            table.hAlign = self.hTableAlignment
        return table

    def layoutFullWidthTable(self,
                             frameInfo,
                             hTableAlignment=TA_CENTER,
                             marginSide=1.8*cm,
                             ratios=[0.3, 0.4, 0.3]):
        """
        Returns a table flowable that spans to frame width.

        :param styledTable: a styled table
        :type styledTable: StyledTable

        :returns: a table flowable element
        """
        # workaround for any too large leftpadding --->
        self.addTableStyleCommand(
            ('LEFTPADDING', (0, 0), (-1, -1), 0 * cm))
        tableStyle = self.handleStyleCommands()
        # columnWidths = self.columnWidthEstim(self.tableData)
        frameWidth = frameInfo._aW - (frameInfo._x1 * 2.)  # -(frameInfo._leftPadding+frameInfo._rightPadding)
        #if self.reportType == "campaign" or self.reportType == "release":
        # NOTE remove workaround later ...
        # print(frameWidth, marginSide)
        frameWidth *= (1.0 - marginSide/frameWidth)

        # prepare columnWidths so that they fit on frameWidth and obey ratios
        if sum(ratios) == 1.:
            expectedWidths = [r * frameWidth for r in ratios]
        else:
            expectedWidths = None
            logger.lpg(lvl="WARNING",
                       msg="ratios of styled meta table unbalanced", orig=self.cn)
        # newColWidths = []
        # if expectedWidths:
        #    for real, avail in zip(columnWidths, expectedWidths):
        #        if not real > avail:
        #            newColWidths.append(avail)
        if self.leftTablePadding > 0:
            expectedWidths.insert(0, self.leftTablePadding)
        table = Table(self.tableData, colWidths=expectedWidths)
        table.setStyle(tableStyle)
        table.hAlign = hTableAlignment
        return table

    def layoutStyledTable(self, hTableAlignment=None, colWidths=None,
                          spaceBefore=None, spaceAfter=None, rightPadding=0,
                          pre=False):
        """
        Returns a table flowable with automatically estimated column width.

        :param styledTable: a styled table
        :type styledTable: StyledTable
        :param hTableAlignment: the table alignment on the frame
        :type hTableAlignment: int
        :param colWidths: the columns width in cm, flexible width is -1
        :type colWidths: list
        :param spaceBefore: the space above the table in cm
        :type spaceBefore: float
        :param spaceAfter: the space below the table in cm
        :type spaceAfter: float

        :returns: a table flowable element
        """
        # styledTable.fontsize = 10

        # general right padding in cells:
        if rightPadding:
            self.rightPadding = rightPadding
        self.addTableStyleCommand(
            ('RIGHTPADDING', (0, 0), (-1, -1), self.rightPadding * cm))
        # BUG: VALIGN does not work with different font sizes !!!
        # styledTable.addTableStyleCommand(
        #    ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'))
        # styledTable.addTableStyleCommand(
        #    ('SIZE', (0, 0), (-1, -1), styledTable.fontsize))
        if hTableAlignment is not None:
            self.hTableAlignment = hTableAlignment

        if colWidths is not None:
            self.colWidths = colWidths
        else:
            colWidths = self.colWidths
        # repair here the leftTablePadding option and the fact that the table data is
        # provided with an additional empty column at the left side
        if colWidths is not None:
            estColWidths = self.columnWidthEstim(self.tableData)
            if self.colsCount() > len(colWidths):
                if isinstance(colWidths, tuple):
                    colWidths = list(colWidths)
                colWidths.insert(0, estColWidths[0])
            while -1 in colWidths:
                i = colWidths.index(-1)
                colWidths[i] = estColWidths[i] / cm
            colWidthsResult = [x * cm for x in colWidths]
        else:
            colWidthsResult = None

        if spaceBefore is not None:
            self.spaceBefore = spaceBefore
        if spaceAfter is not None:
            self.spaceAfter = spaceAfter
        if pre:
            # NOTE returns the style table again
            return self
        else:
            table = Table(self.tableData, colWidths=colWidthsResult,
                            spaceBefore=self.spaceBefore * cm, spaceAfter=self.spaceAfter * cm)
            tableStyle = self.handleStyleCommands()
            table.setStyle(tableStyle)
            table.hAlign = self.hTableAlignment
            return table

    def columnWidthEstim(self, data):
        """
        Returns minimum column width for all lines in the column.

        :param data: the table data
        :type data: list of list

        :returns: list of cell width estimations
        """
        cell_widths = defaultdict(int)

        for line in data:
            for i, cell in enumerate(line):
                cell_width_est = self.widthEstim(cell)
                if cell_width_est > cell_widths[i]:
                    cell_widths[i] = cell_width_est

        return [cell_widths[i] for i in range(len(list(cell_widths)))]


    def widthEstim(self, obj, name="table"):
        """
        Estimates the width of an object.
        If obj is of type str: estimates the width of the text on page, using the self.font
        If object is of type reportlab.Flowable, then return the result of minWidth()

        :param obj: the object which will be estimated
        :type obj: object
        :param name: the name of the fontszize
        :type name: str

        :returns: the estimated width
        """
        if isinstance(obj, (float, int)):
            return int(
                self.font.stringWidth("%s" % obj, self.fontsize))
        elif isinstance(obj, str):
            # print(obj,np.ceil(self.font.stringWidth(obj,self.fontsizes[name])))
            largestStr = sorted(obj.split("\n"), key=lambda x: len(x))[-1]
            # print(largestStr)
            return int(
                self.font.stringWidth(largestStr, self.fontsize))
        elif isinstance(obj, Flowable):
            return obj.minWidth()
        elif obj is None:
            return 0.
        elif isinstance(obj, list):
            return 100.
        else:
            raise (NotImplementedError(type(obj)))

    def getTableHeight(self, frameInfo):
        """
        Returns height of table hint

        :param table: the table object
        :type table: Table
        """
        return self.as_flowable.wrap(frameInfo._aW, frameInfo._aH)[1]


    def split_table(self, n):
        """
        """
        table_copy_up = copy.deepcopy(self)
        table_copy_down = copy.deepcopy(self)
        table_copy_down.tableData = self.tableData[n:]
        table_copy_down.tableData.insert(0, self.tableData[0])
        table_copy_up.tableData = self.tableData[0:n]
        return table_copy_up, table_copy_down


    def split_table_iterative(self, frameInfo, availableHeight):
        """
        """
        maxHeight = availableHeight - self.spaceBefore * cm - self.spaceAfter * cm
        n = len(self.tableData) - 1
        table_copy_up, table_copy_down = self.split_table(n)
        while table_copy_up.getTableHeight(frameInfo) > maxHeight * 0.9:
            n -= 1
            if n >= 1:
                table_copy_up, table_copy_down = self.split_table(n)
            else:
                break
        table_copy_down.shift_background_styles(n-1)
        table_copy_up.snip_background_styles(n)
        return table_copy_up, table_copy_down

    def shift_background_styles(self, n):
        """
        """
        out_styles = []
        tableStyleCommands = []
        for command in self.tableStyleCommands:
            if command[0] == "BACKGROUND":
                new_command = list(command)
                new_command[1][1] -= n
                new_command[2][1] -= n
                if new_command[1][1] > 0 and new_command[2][1]> 0:
                    tableStyleCommands.append(new_command)
            else:
                tableStyleCommands.append(command)
        self.tableStyleCommands = tableStyleCommands

    def snip_background_styles(self, n):
        """
        """
        out_styles = []
        tableStyleCommands = []
        for command in self.tableStyleCommands:
            if command[0] == "BACKGROUND":
                if command[1][1] < n and command[2][1] < n:
                    tableStyleCommands.append(command)
                    # print(new_command)
            else:
                tableStyleCommands.append(command)
        self.tableStyleCommands = tableStyleCommands
