# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:11:12 2015

@author: johannes
"""
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from io import BytesIO
from functools import wraps
from cycler import cycler

import matplotlib
from autoreport import is_python3
if is_python3:
    matplotlib.use('Qt5Agg')
else:
    matplotlib.use('Agg')

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.ticker import LinearLocator, MultipleLocator, AutoMinorLocator, FormatStrFormatter
import matplotlib.font_manager as fm
from matplotlib.font_manager import findfont
from matplotlib import ft2font
from matplotlib.font_manager import createFontList, ttfFontProperty

# add color names, missing in matplotlib
missing_names = {'darkyellow': '#CC9900',
                 'lightmagenta':'#EDB2ED',
                 'lightred':'#FF8787'}

matplotlib.colors.cnames.update(missing_names)

plt.ioff()

from autoreport.pdfimage import PdfImage, PdfAsset, getScaledSvg

fontprop=None

def autoPdfImage(func):
    """
    decorator for the autoplot module
    
    returns two PdfImage objects if wrapped plt-function obeys the principle
    demonstated in following minimal example::
        
        @autoPdfImage
        def my_plot(canvaswidth=5): #[inch]
            fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
            fig.suptitle("My Plot",fontproperties=fontprop)
            x=[1,2,3,4,5,6,7,8]
            y=[1,6,8,3,9,3,4,2]
            ax.plot(x,y,label="legendlabel")
            nrow,ncol=1,1
            handels,labels= ax.get_legend_handles_labels()
            
            leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))
            
            leg = leg_fig.legend(handles, labels, #labels = tuple(bar_names)
                   ncol=ncol, mode=None,
                   borderaxespad=0.,
                   loc='center',        # the location of the legend handles
                   handleheight=None,   # the height of the legend handles
                   #fontsize=9,         # prop beats fontsize
                   markerscale=None,
                   frameon=False,
                   prop=fontprop
                   #fancybox=True,
                   )
            
            return fig,leg_fig,leg
    
    TODO: add example in tests
    """
    @wraps(func)
    def funcwrapper(*args,**kwargs):
        """
        minimal example::
            
            def my_decorator(f):
                @wraps(f)
                def wrapper(*args, **kwds):
                    print('Calling decorated function')
                    return f(*args, **kwds)
                return wrapper
        """
        imgax = BytesIO()
        imgleg = BytesIO()
        
        fig, leg_fig, leg = func(*args, **kwargs)
        
        if not fig:
            return
        
        leg_fig.savefig(imgleg,
                        additional_artists=(leg.get_window_extent(),),
                        bbox_extra_artists=(leg.legendPatch,),
                        bbox_inches='tight',
                        format='PDF',
                        transparent=True)
        # rewind the data
        imgleg.seek(0)
        
        plt.clf()
        plt.close('all')
        fig.savefig(imgax, format='PDF')
        return PdfImage(imgax), PdfImage(imgleg)
    return funcwrapper

def full_extent(ax, pad=0.0):
    """
    Get the full extent of an axes, including axes labels, tick labels, and
    titles.
    """
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    try:
        items = ax.get_xticklabels() + ax.get_yticklabels()
    except AttributeError:
        return ax.get_window_extent()
    # items += [ax, ax.title, ax.xaxis.label, ax.yaxis.label]
    items += [ax, ax.title]
    bbox = Bbox.union([item.get_window_extent() for item in items])
    return bbox.expanded(1.0 + pad, 1.0 + pad)
