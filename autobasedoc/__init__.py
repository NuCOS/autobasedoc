# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:40:26 2015

This package is a set of helper functions and classes around autorpt.AutoBaseDoc

the two main modules provided by this package are:

* autorpt   provides a Reportlab AutoBaseDoc, a Document Template Class derived from reportlab's BaseDocTemplate
* autoplt   provides decorators for matplotlib functions to make them return pdf-image-flowables

You should import the two modules directly::

import autobasedoc.autorpt as ar
import autobasedoc.autoplot as ap
from autobasedoc.autorpt import base_fonts, addPlugin

@author: oliver, johannes
"""
import sys
from .version import version

from reportlab.lib import colors
from reportlab.lib.colors import Color

__version__ = version
__license__ = __doc__
is_python3 = (sys.version_info.major == 3)
_baseFontNames = dict(normal='Helvetica',
                      bold='Helvetica-Bold',
                      italic='Helvetica-Oblique',
                      bold_italic='Helvetica-BoldOblique')

_color_dict = {}

def setup_color_dict(colors):
    """
    setup colors
    only adding items where key is str AND value is Color to the color_dict
    """
    for k, v in vars(colors).items():
        if isinstance(k, str) and isinstance(v, Color):
            _color_dict.update({k: v})

    _color_dict.update({
        'gray40': Color(0.4, 0.4, 0.4, 1),
        'lightred': Color(.980392, .501961, .447059, 1)
        })

setup_color_dict(colors)

def base_fonts():
    """
    there should be one base font per document
    this is how to obtain that dictionary
    of the different font weights of that base font
    """
    return _baseFontNames

def color_dict():
    """
    base colors
    """
    return _color_dict
