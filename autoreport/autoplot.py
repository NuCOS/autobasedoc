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

import numpy as np

#from scipy.stats import gaussian_kde
#from scipy.stats import kurtosis
#from scipy.stats import variation
#from scipy.stats import skew

if __name__ == "__main__":
    pass
    #import shutil
    
    #shutil.rmtree(r"C:\Users\ecksjoh\.matplotlib")

import matplotlib
is_python3 = ( sys.version_info.major==3 )
if is_python3:
    matplotlib.use('Qt5Agg')
else:
    matplotlib.use('Agg')

# Farbnamen, die in Matplotlib fehlen, ergänzen
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

plt.ioff()

#from matplotlib import verbose
#verbose.set_level('debug')

#print(_basePath)
#print("autoplot data path:",matplotlib.rcParams['datapath'])

from cycler import cycler

plotcolors=['#4169E1',  #royalblue
            '#FF6347',  #tomato
            '#FFD700',  #gold
            '#48D1CC',  #mediumturquosie
            '#BA55D3',  #mediumorchid
            '#9ACD32',  #yellowgreen
            '#DEB887',  #burlywood
            '#2F4F4F',  #darkslategray
            '#FFA500',  #orange
            '#C0C0C0',  #silver
            ]

#almost_black='#262626'
almost_black='#000000'

textsize = 12

#plt.rc('axes', color_cycle=plotcolors)
matplotlib.rc('axes', prop_cycle=(cycler('color', plotcolors)))

plt.rc('xtick', labelsize=textsize,color=almost_black)
plt.rc('ytick', labelsize=textsize, color=almost_black)

from pdfimage import PdfImage,PdfAsset,getScaledSvg

__font_dir__ = os.path.dirname(__file__)
__font_dir__ = os.path.realpath(os.path.join(__font_dir__,"fonts"))

font = fm.FontProperties(
        family = 'sans-serif', fname = os.path.join(__font_dir__,'calibri.ttf'))

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'calibri'
matplotlib.rcParams['font.style'] = 'normal'

#plotcolors=['darkslategray','salmon','royalblue','lawngreen', 'gold','cyan','violet']
#plotcolors+=plotcolors

properties={}

properties.update({"labelAxesFontSize":12,
                   "tickAxesFontSize":12,
                   "legendLabelFontSize":12,
                   "textBoxFontSize":12,
                   "titleFontSize":12,
                   "textTableFontSize":12})

textsize=12

def autoPdfImage(func):
    """
    decorator for the autoplot module
    """
    def funcwrapper(*args,**kwargs):
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