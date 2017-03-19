# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 11:11:12 2015

@author: ecksjoh
"""
from __future__ import print_function
from __future__ import unicode_literals

from io import BytesIO

import os
import sys

#from itertools import cycle
#from operator import itemgetter, attrgetter

#import numpy as np

#from scipy.stats import gaussian_kde
#from scipy.stats import kurtosis
#from scipy.stats import variation
#from scipy.stats import skew

#import shutil

#shutil.rmtree(os.path.join(os.path.expanduser("~"),".matplotlib"))

import matplotlib
is_python3 = ( sys.version_info.major==3 )
if is_python3:
    matplotlib.use('Qt5Agg')
else:
    matplotlib.use('Agg')

# add color names, missing in matplotlib
matplotlib.colors.cnames.update({'darkyellow': '#CC9900', 'lightmagenta':'#EDB2ED', 'lightred':'#FF8787'})

#print( plt.get_backend() )

#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['pdf.use14corefonts'] = True
#
matplotlib.rcParams['axes.unicode_minus']=False

#basePath = os.path.dirname(os.path.realpath(os.path.join(__file__,"../")))
#matplotlib.rcParams['datapath']=os.path.join(basePath,"mpl-data")
#print(basePath)

#import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from matplotlib.transforms import Bbox

#from matplotlib import ticker
from matplotlib.ticker import LinearLocator,MultipleLocator,AutoMinorLocator,FormatStrFormatter
##from matplotlib.ticker import 
import matplotlib.font_manager as fm

from matplotlib.font_manager import findfont
from matplotlib import ft2font

from matplotlib.font_manager import createFontList, ttfFontProperty

plt.ioff()

#from matplotlib import verbose
#verbose.set_level('debug')

#print(_basePath)
#print("autoplot data path:",matplotlib.rcParams['datapath'])

from cycler import cycler

#plotcolors=['#4169E1',  #royalblue
#            '#FF6347',  #tomato
#            '#FFD700',  #gold
#            '#48D1CC',  #mediumturquosie
#            '#BA55D3',  #mediumorchid
#            '#9ACD32',  #yellowgreen
#            '#DEB887',  #burlywood
#            '#2F4F4F',  #darkslategray
#            '#FFA500',  #orange
#            '#C0C0C0',  #silver
#            ]

#almost_black='#262626'
#almost_black='#000000'

#plt.rc('axes', color_cycle=plotcolors)
#matplotlib.rc('axes', prop_cycle=(cycler('color', plotcolors)))

textsize = 12
#plt.rc('xtick', 
#       labelsize=textsize,
#       color=almost_black)
#plt.rc('ytick', 
#       labelsize=textsize, 
#       color=almost_black)

from pdfimage import PdfImage,PdfAsset,getScaledSvg

from functools import wraps

__font_dir__ = os.path.dirname(__file__)
__font_dir__ = os.path.realpath(os.path.join(__font_dir__,"fonts"))

#font = fm.FontProperties(family = 'sans-serif', 
#                         fname = os.path.join(__font_dir__,'calibri.ttf'))

#fpath = os.path.join(__font_dir__,'c063002t.ttf')
#font = ft2font.FT2Font(fpath)
#fontprop = ttfFontProperty(font)

fontprop=None

#print(fontprop.get_name())

#matplotlib.rcParams['font.family'] = 'sans-serif'
#matplotlib.rcParams['font.sans-serif'] = font.get_name()
#matplotlib.rcParams['font.style'] = 'normal'

#plotcolors=['darkslategray','salmon','royalblue','lawngreen', 'gold','cyan','violet']
#plotcolors+=plotcolors

#properties={}
#
#properties.update({"labelAxesFontSize":textsize,
#                   "tickAxesFontSize":textsize,
#                   "legendLabelFontSize":textsize,
#                   "textBoxFontSize":textsize,
#                   "titleFontSize":textsize,
#                   "textTableFontSize":textsize})

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
            handels,labels= axl.get_legend_handles_labels()
            
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
        
        fig,leg_fig,leg = func(*args, **kwargs)
        
        if not fig:
            return
        
        #canvaswidth = kwargs["canvaswidth"]
        #leg_fig = plt.figure(figsize=(canvaswidth, 0.2*leg.nrow))
        
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
        fig.savefig(imgax,format='PDF')
        return PdfImage(imgax),PdfImage(imgleg)
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
    
if __name__== "__main__":
    pass