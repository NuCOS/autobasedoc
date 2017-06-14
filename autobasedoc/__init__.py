# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 11:40:26 2015

@author: ecksjoh
"""
import sys
import autobasedoc.version as version

__version__ = version.version
__license__ = __doc__
is_python3 = (sys.version_info.major == 3)
_baseFontNames = dict(normal='Helvetica',
                      bold='Helvetica-Bold',
                      italic='Helvetica-Oblique',
                      bold_italic='Helvetica-BoldOblique')

import autobasedoc.autorpt as ar
import autobasedoc.autoplot as ap
