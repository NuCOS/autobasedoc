# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:40:26 2015

@author: ecksjoh
"""
import sys
from .version import version

__version__ = version
__license__ = __doc__
is_python3 = (sys.version_info.major == 3)
_baseFontNames = dict(normal='Helvetica',
                      bold='Helvetica-Bold',
                      italic='Helvetica-Oblique',
                      bold_italic='Helvetica-BoldOblique')

def base_fonts():
    """
    there should be one base font per document
    this is how to obtain that dictionary
    of the different font weights of that base font
    """
    return _baseFontNames
