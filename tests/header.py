
import autobasedoc.autorpt as ar
import copy


class Header(ar.StyledTable):
    """
    data object to store all data of header of one page
    """

    def __init__(self, title=None, headerMarginTop=0.5, debug=False):
        """

        """
        super(Header, self).__init__()
        self.headerMarginTop = headerMarginTop  # in cm
        self.title = title
        self.figure_left = ""
        self.right_lines = [[""]]
        self.tableData = [["", "", ""]]
        self.tableStyleCommands = list()
        self.addTableStyleCommand(('FONT', (0, 0), (-1, -1),
                                   ar._baseFontNames['normal']))
        self.addTableStyleCommand(('FONTSIZE', (0, 0), (-1, -1),
                                   10))

        # NOTE: for debugging spaces:
        self.debug = debug
        if debug:
            self.addTableStyleCommand(
                ("GRID", (0, 0), (-1, -1), 0.5, ar.colors.black))
        self.addTableExtraStyleCommand(('TOPPADDING', (0, 0),
                                        (-1, -1), 0 * ar.cm))
        self.addTableExtraStyleCommand(('RIGHTPADDING', (0, 0),
                                        (-1, -1), 0 * ar.cm))
        self.addTableExtraStyleCommand(('BOTTOMPADDING', (0, 0),
                                        (-1, -1), 0 * ar.cm))
        self.addTableExtraStyleCommand(('LEFTPADDING', (0, 0),
                                        (-1, -1), 0 * ar.cm))
        self.addTableExtraStyleCommand(('ALIGN', (2, 0),
                                        (2, 0), 'RIGHT'))

    def setTitle(self, title):
        """
        Sets the title for page element.

        :param title: the title of the element
        :type title: str
        """
        self.title = title

    @property
    def margin_top(self):
        return ar.Spacer(width=2.0 * ar.cm, height=self.headerMarginTop * ar.cm)

    def height(self, frameInfo):
        return self.as_flowable.wrap(frameInfo._aW, frameInfo._aH)[1] + self.headerMarginTop * ar.cm

    def headerBuild(self, headerLines, figure_left=None, right_lines=None):
        """
        Generates a styled header
        (in the END FDM and LDM header should be equally designed)

        """
        header = copy.deepcopy(self)
        title = copy.copy(headerLines[0][1])
        if figure_left:
            header.figure_left = figure_left
            self.figure_left = figure_left
        headerLines[0][0] = self.figure_left
        if right_lines:
            header.right_lines = right_lines
        rightStack = ar.StyledTable(leftTablePadding=0, gridded=self.debug)
        rightStack.addTableExtraStyleCommand(
            ("FONTSIZE", (0, 0), (-1, -1), 11))  # DEFAULT FONT SIZE
        rightStack.addTableExtraStyleCommand(
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"))
        rightStack.addTableExtraStyleCommand(
            ("VALIGN", (0, 0), (-1, -1), "TOP"))
        rightStack.addTableExtraStyleCommand(('RIGHTPADDING', (0, 0),
                                              (-1, -1), 0 * ar.cm))
        rightStack.addTableExtraStyleCommand(('TOPPADDING', (0, 0),
                                              (-1, -1), -0.11 * ar.cm))
        rightStack.addTableExtraStyleCommand(('BOTTOMPADDING', (0, 0),
                                              (-1, -1), 0.23 * ar.cm))
        # TODO eas for correct font
        # rightStack.addTableExtraStyleCommand(
        #    ('FONT', (0, 1), (0, 1), ar._baseFontNames["bold"]))
        rightStack.setTableData(header.right_lines)
        headerLines[0][-1] = rightStack.layoutStyledTable()

        header.setTableData(headerLines)
        header.addTableStyleCommand(("ALIGN", (1, 0), (1, 0), "CENTER"))
        header.addTableStyleCommand(("SIZE", (1, 0), (1, 0), 20))  # FONT SIZE of the MAIN Title
        header.addTableStyleCommand(
            ("FONT", (1, 0), (1, 0), ar._baseFontNames["bold"]))
        header.addTableStyleCommand(("ALIGN", (0, 0), (0, 0), "LEFT"))
        header.addTableStyleCommand(("ALIGN", (2, 0), (2, 0), "RIGHT"))
        header.addTableExtraStyleCommand(("VALIGN", (0, 0), (-1, -1), "TOP"))
        header.addTableExtraStyleCommand(('TOPPADDING', (0, 0),
                                          (-1, -1), 0 * ar.cm))
        header.addTableExtraStyleCommand(('RIGHTPADDING', (0, 0),
                                          (-1, -1), 0 * ar.cm))
        header.addTableExtraStyleCommand(('BOTTOMPADDING', (0, 0),
                                          (-1, -1), 0 * ar.cm))
        header.addTableExtraStyleCommand(('LEFTPADDING', (0, 0),
                                          (-1, -1), 0 * ar.cm))

        # self.addHorizontalLines()
        return header, title
