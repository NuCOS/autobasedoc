"""

footer
------

.. module:: footer
   :platform: Unix, Windows
   :synopsis: specialized for footer

Created 2016, 2017

@author: johannes

"""
import copy
import autobasedoc.autorpt as ar
from plot_tools import importSVG


class Footer(ar.StyledTable):
    """
    data object to store all data of footer of one page
    """

    def __init__(self, title=None, footerMarginBottom=0.5, debug=False):
        """

        """
        super(Footer, self).__init__()
        self.footerMarginBottom = footerMarginBottom  # in cm
        self.title = title
        self.figureFiles = []
        self.tableData = [["", "", "", ""]]
        self.tableStyleCommands = list()
        self.addTableStyleCommand(('FONT', (0, 0), (-1, -1),
                                   ar._baseFontNames['normal']))
        self.addTableStyleCommand(('FONTSIZE', (0, 0), (-1, -1),
                                   10))

        # NOTE: for debugging spaces:
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
        # self.addTableExtraStyleCommand(('ALIGN', (3, 0),
        #                                 (3, 0), 'RIGHT'))

    def setTitle(self, title):
        """
        Sets the title for page element.

        :param title: the title of the element
        :type title: str
        """
        self.title = title

    def margin_top(self, frameInfo, offsetheight):
        sHeight = frameInfo._aH - \
            (self.as_flowable.wrap(frameInfo._aW, frameInfo._aH)
             [1] + self.footerMarginBottom * ar.cm)
        # print(".....", offsetheight, sHeight)
        # sHeight = 300
        return ar.Spacer(width=frameInfo._aW, height=sHeight - offsetheight)

    def footerBuild(self, lines, figureFiles=None):
        """
        Adds default pictograms to footer (user, date and filename)
        """
        lines = copy.deepcopy(lines)  # prevent funny behaviour
        self.setTableData(lines)
        if figureFiles:
            self.figureFiles = figureFiles
        for i, figureFile in enumerate(self.figureFiles):
            if figureFile.endswith(".svg"):
                userFigure = importSVG(
                    figureFile,
                    scale=1.0,
                    width=10,
                    height=10)
            else:
                userFigure = figureFile # means as text!
            self.tableData[0][i] = self.figureTextCombination(
                userFigure, self.tableData[0][i])
        last_index = len(self.tableData[0]) - 1
        # align text in the last column to the right
        self.addTableExtraStyleCommand(('ALIGN', (last_index, 0),
                                        (last_index, 0), 'RIGHT'))
        self.addTableExtraStyleCommand(('ALIGN', (last_index-1, 0),
                                        (last_index-1, 0), 'RIGHT'))
        return copy.deepcopy(self)

    def figureTextCombination(self, figure, text, align="left"):
        """
        Builds and returns a tight svg-text table as a combined table line-object

        """
        rightTable = ar.StyledTable(leftTablePadding=0, gridded=False)
        rightTable.setTableData([[figure, text]])
        rightTable.addTableExtraStyleCommand(('BOTTOMPADDING', (0, 0),
                                              (-1, -1), 0 * ar.cm))
        rightTable.addTableExtraStyleCommand(('LEFTPADDING', (0, 0),
                                              (-1, -1), 0. * ar.cm))
        rightTable.addTableExtraStyleCommand(('RIGHTPADDING', (0, 0),
                                              (-1, -1), 0. * ar.cm))
        rightTable.addTableExtraStyleCommand(('TOPPADDING', (0, 0),
                                              (-1, -1), 0. * ar.cm))
        if align == "left":
            rightTable.addTableExtraStyleCommand(('LEFTPADDING', (1, 0),
                                                  (1, 0), 0.1 * ar.cm))
        else:
            rightTable.addTableExtraStyleCommand(('LEFTPADDING', (1, 0),
                                                  (1, 0), 0.1 * ar.cm))
        if align == "left":
            rightTable.addTableExtraStyleCommand(
                ("ALIGN", (1, 0), (1, 0), "LEFT"))
        else:
            rightTable.addTableExtraStyleCommand(
                ("ALIGN", (1, 0), (1, 0), "RIGHT"))
        rightTable.addTableExtraStyleCommand(
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"))
        rightTable.addTableExtraStyleCommand(('RIGHTPADDING', (0, 0),
                                              (0, 0), 0.1 * ar.cm))
        rightTable.addTableExtraStyleCommand(('BOTTOMPADDING', (0, 0),
                                              (0, 0), 0.05 * ar.cm))
        stackLine = rightTable.layoutStyledTable(
            rightTable, colWidths=[12 / ar.cm, -1], factor=1.1)
        return stackLine
