# -*- coding: utf-8 -*-
"""
autoplot
========

.. module:: autoplot
   :platform: Unix, Windows
   :synopsis: decorator to wrap around matplotlib plot functions into flowables

.. moduleauthor:: Johannes Eckstein

Created on Wed Sep 16 11:11:12 2015
"""
import os
import sys

from io import BytesIO
from functools import wraps
from cycler import cycler

import matplotlib

# try:
#     matplotlib.use('Agg', force=True)
# except:
#     print("check your matplotlib aggregator settings")
#     print("matplotlib version:", matplotlib.__version__)

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.ticker import LinearLocator, MultipleLocator, AutoMinorLocator, FormatStrFormatter
import matplotlib.font_manager as fm
from matplotlib.font_manager import findfont
from matplotlib import ft2font
from matplotlib.font_manager import ttfFontProperty

from autobasedoc.pdfimage import PdfImage, PdfAsset, getScaledSvg

# add color names, missing in matplotlib
missing_names = {
    'darkyellow': '#CC9900',
    'lightmagenta': '#EDB2ED',
    'lightred': '#FF8787'
}

matplotlib.colors.cnames.update(missing_names)

plt.ioff()

fontprop = None


def autoPdfImage(func):
    """Decorator returning :class:`PdfImage` instances for plots.

    The wrapped matplotlib function must return a tuple ``(fig, legend_fig,
    legend)``.  Two :class:`PdfImage` objects – the plot and its legend – are
    produced.  Example::

        @autoPdfImage
        def my_plot(canvaswidth=5): #[inch]
            fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
            fig.suptitle("My Plot",fontproperties=fontprop)
            x=[1,2,3,4,5,6,7,8]
            y=[1,6,8,3,9,3,4,2]
            ax.plot(x,y,label="legendlabel")
            nrow,ncol=1,1
            handles, labels = ax.get_legend_handles_labels()

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
    def funcwrapper(*args, **kwargs):
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

        leg_fig.savefig(
            imgleg,
            #additional_artists=(leg.get_window_extent(), ),
            bbox_extra_artists=(leg.legendPatch, ),
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


def autoPdfImg(func):
    """Decorator returning a single :class:`PdfImage` for a plot.

    The wrapped function should return a matplotlib ``Figure``.  The figure is
    saved to a PDF byte buffer and returned as a :class:`PdfImage`.  Example::

        @autoPdfImg
        def my_plot(canvaswidth=5): #[inch]
            fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
            fig.suptitle("My Plot",fontproperties=fontprop)
            x=[1,2,3,4,5,6,7,8]
            y=[1,6,8,3,9,3,4,2]
            ax.plot(x,y,label="legendlabel")
            nrow,ncol=1,1
            handles, labels = ax.get_legend_handles_labels()

            leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))

            ax.legend(handles, labels, #labels = tuple(bar_names)
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

            return fig

    """

    @wraps(func)
    def funcwrapper(*args, **kwargs):
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

        fig = func(*args, **kwargs)

        if not fig:
            return

        plt.clf()

        if 'close' in kwargs:
            if kwargs['close']:
                plt.close('all')
        fig.savefig(imgax, format='PDF')

        return PdfImage(imgax)

    return funcwrapper


def full_extent(ax, pad=0.0):
    """Return the bounding box of an ``Axes`` including tick and axis labels.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        Target axes instance.
    pad : float, optional
        Padding factor applied to the final bounding box.
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
