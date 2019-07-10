"""
styles
======

.. module:: styles
   :platform: Unix, Windows
   :synopsis: predefined styles for easy configuration

.. moduleauthor:: Johannes Eckstein
"""
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from autobasedoc import base_fonts

# A Class to control the behaviour of the styles object
_stylesheet1_undefined = object()


class StyleSheet:
    """
    This may or may not be used.  The idea is to:

    1. slightly simplify construction of stylesheets;

    2. enforce rules to validate styles when added
       (e.g. we may choose to disallow having both
       'heading1' and 'Heading1' - actual rules are
       open to discussion);

    3. allow aliases and alternate style lookup
       mechanisms

    4. Have a place to hang style-manipulation
       methods (save, load, maybe support a GUI
       editor)

    Access is via getitem, so they can be
    compatible with plain old dictionaries.
    """

    def __init__(self):
        self.byName = {}
        self.byAlias = {}

    def __getitem__(self, key):
        try:
            return self.byAlias[key]
        except KeyError:
            try:
                return self.byName[key]
            except KeyError:
                raise KeyError("Style '%s' not found in stylesheet" % key)

    def get(self, key, default=_stylesheet1_undefined):
        try:
            return self[key]
        except KeyError:
            if default != _stylesheet1_undefined: return default
            raise

    def __contains__(self, key):
        return key in self.byAlias or key in self.byName

    def has_key(self, key):
        return key in self

    def add(self, style, alias=None):
        key = style.name
        if key in self.byName and key in self.byAlias:
            raise KeyError("Style key '%s' already defined in stylesheet" %
                           key)

        if alias:
            if alias in self.byName:
                raise KeyError("Style '%s' already defined in stylesheet" %
                               alias)
            if alias in self.byAlias:
                raise KeyError(
                    "Alias name '%s' is already an alias in stylesheet" %
                    alias)

            style.alias = alias
        #passed all tests?  OK, add it
        self.byName[key] = style
        if alias:
            self.byAlias[alias] = style

    def list(self):
        styles = list(self.byName.items())
        styles.sort()
        alii = {}
        for (alias, style) in list(self.byAlias.items()):
            alii[style] = alias
        for (name, style) in styles:
            alias = alii.get(style, None)
            print(name, alias)


# Define Styles
class Styles(object):
    """
    default styles definition

    provides a function to easily register more styles
    """
    def __init__(self):

        self.stylesheet = StyleSheet()

        self.addStyle(
            ParagraphStyle(
                name='Normal',
                fontName=base_fonts()["normal"],
                fontSize=10,
                bulletFontName=base_fonts()["normal"],
                leading=12))
        self.addStyle(
            ParagraphStyle(
                name='BodyText',
                parent=self.stylesheet['Normal'],
                spaceBefore=6),
            alias='normal')

        self.addStyle(
            ParagraphStyle(
                name='Table', parent=self.stylesheet['Normal'], spaceBefore=0),
            alias='table')

        self.addStyle(
            ParagraphStyle(
                name='Italic',
                parent=self.stylesheet['BodyText'],
                fontName=base_fonts()["italic"]),
            alias='italic')

        self.addStyle(
            ParagraphStyle(
                name='Bold',
                parent=self.stylesheet['BodyText'],
                fontName=base_fonts()["bold"]),
            alias='bold')

        self.addStyle(
            ParagraphStyle(
                name='Centered',
                parent=self.stylesheet['BodyText'],
                alignment=TA_CENTER),
            alias='centered')

        self.addStyle(
            ParagraphStyle(
                name='Right',
                parent=self.stylesheet['BodyText'],
                alignment=TA_RIGHT,
                wordWrap=False),
            alias='right')

        self.addStyle(
            ParagraphStyle(
                name='Title',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=18,
                leading=22,
                alignment=TA_CENTER,
                spaceAfter=6),
            alias='title')

        self.addStyle(
            ParagraphStyle(
                name='Heading1',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=18,
                leading=22,
                spaceAfter=6),
            alias='h1')

        self.addStyle(
            ParagraphStyle(
                name='Heading2',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=14,
                leading=18,
                spaceBefore=12,
                spaceAfter=6),
            alias='h2')

        self.addStyle(
            ParagraphStyle(
                name='Heading3',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=12,
                leading=14,
                spaceBefore=12,
                spaceAfter=6),
            alias='h3')

        self.addStyle(
            ParagraphStyle(
                name='Heading4',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=10,
                leading=12,
                spaceBefore=10,
                spaceAfter=4),
            alias='h4')

        self.addStyle(
            ParagraphStyle(
                name='Heading5',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=9,
                leading=10.8,
                spaceBefore=8,
                spaceAfter=4),
            alias='h5')

        self.addStyle(
            ParagraphStyle(
                name='Heading6',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                fontSize=7,
                leading=8.4,
                spaceBefore=6,
                spaceAfter=2),
            alias='h6')

        self.addStyle(
            ParagraphStyle(
                name='Heading6',
                parent=self.stylesheet['Normal'],
                fontName=base_fonts()["bold"],
                alignment=TA_CENTER,
                fontSize=12,
                leading=8.4,
                spaceBefore=14,
                spaceAfter=2),
            alias='caption')

        self.addStyle(
            ParagraphStyle(
                name='Bullet',
                parent=self.stylesheet['Normal'],
                firstLineIndent=0,
                spaceBefore=3),
            alias='bu')

        self.addStyle(
            ParagraphStyle(
                name='Definition',
                parent=self.stylesheet['Normal'],
                firstLineIndent=0,
                leftIndent=36,
                bulletIndent=0,
                spaceBefore=6,
                bulletFontName=base_fonts()["bold_italic"]),
            alias='df')

        self.addStyle(
            ParagraphStyle(
                name='Code',
                parent=self.stylesheet['Normal'],
                fontName='Courier',
                alignment=TA_LEFT,
                fontSize=8,
                leading=8.8,
                firstLineIndent=0,
                leftIndent=36),
            alias='code')

        self.addStyle(
            ParagraphStyle(
                name='ConsoleText',
                parent=self.stylesheet['Normal'],
                fontName='Courier',
                alignment=TA_LEFT,
                fontSize=11,
                leading=14,  #16
                firstLineIndent=0,
                leftIndent=0,
                spaceBefore=2,
                spaceAfter=0),
            alias='console')

        self.addStyle(
            ParagraphStyle(
                name='Warning',
                parent=self.stylesheet['Normal'],
                fontName='Courier',
                alignment=TA_LEFT,
                fontSize=11,
                textColor='red',
                leading=14,  #16
                firstLineIndent=0,
                leftIndent=10,
                spaceBefore=0,
                spaceAfter=0),
            alias='warning')
        # Fixed Notation
        self.p2 = ParagraphStyle(
            name='Heading2',  # must be according to TOC depth
            parent=self.stylesheet['Normal'],
            fontSize=10,
            leading=12)

        self.p3 = ParagraphStyle(
            name='Heading3',  # must be according to TOC depth
            parent=self.stylesheet['Normal'],
            fontSize=10,
            leading=12)

    def addStyle(self, PS, alias=None):
        """
        add a ParagraphStyle to stylesheet
        """
        self.stylesheet.add(PS, alias=alias)

    def registerStyles(self):
        """
        register all stylesheets by their respective aliases
        """
        for style_name in self.stylesheet.byAlias:
            setattr(self, style_name, self.stylesheet[style_name])

    def listAttrs(self, style, indent=''):
        """
        print all registered styles
        """
        print(indent + 'name = ' + str(style.name))
        print(indent + 'parent = ' + str(style.parent))
        keylist = sorted(list(vars(style).keys()))
        keylist.remove('name')
        keylist.remove('parent')
        for key in keylist:
            value = vars(style).get(key, None)
            print(indent + '%s = %s' % (key, value))

    def listStyles(self):
        """
        return list of styles in object
        """
        keylist = sorted(list(vars(self)))
        keylist.remove('stylesheet')

        return keylist

    def StyleInfoByAlias(self, alias):
        """
        prints all attributes of a style matching the alias
        """
        style = self.__getattribute__(alias)
        try:
            print("test", style.name)
            self.listAttrs(style, indent="   ")
        except AttributeError:
            pass
