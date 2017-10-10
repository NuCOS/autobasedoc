.. _basic_usage:

Basic Usage
===========

.. sidebar:: Short

    - There are actually two modules: *autoplot* and *autorpt* 
    - The principle usage is shown in the tests and the example

.. index:: Basic Usage

Reportlab-Suite
---------------

To work with the reportlab-toolbox you should import the following:

.. code-block:: python

    from autobasedoc import ar

A usual working example for creating just a simple (empty) pdf file with a title-page and a table of contents would be:

.. code-block:: python

    import os
    outname = os.path.join(os.path.dirname(__file__), "MinimalExample.pdf")
    doc = ar.AutoDocTemplate(outname,onFirstPage=ar.drawLaterPage,onLaterPages=ar.drawLaterPage,onLaterSPages=ar.drawLaterPage,
                            leftMargin=0.5*ar.cm, rightMargin=0.5*ar.cm, topMargin=0.5*ar.cm, bottomMargin=0.5*ar.cm)

    #  you always work with your styles object
    styles = ar.Styles()
    styles.registerStyles()

    #  the container for the contents, also commonly called the story (contains reportlab flowables)
    content = []
    #add title
    para = ar.Paragraph(u"Minimal Example Title", styles.title)
    content.append(para)
    content.append(ar.PageBreak())

    #  create table of contents. Override the level styles (optional)
    toc = ar.doTabelOfContents()
    content.append(ar.Paragraph(u"Table Of Contents", styles.h1))
    content.append(toc)

    #  always call multi build at the end
    doc.multiBuild(content)

ttf-Fonts
---------

To work with ttf-fonts and have the same font inside your matplotlib images and reportlab.platypus you have to use the following code block:

.. code-block:: python

    import os  #  if you haven't, yet.
    # we assume you have a fonts path 
    # (if you haven't you can use the calibri font we added to the module) ar.__font_dir__
    # the ap (autoplot) module provides helpful stuff for combining reportlab with matplotlib
    from autobasedoc import ap

    #  here should be your path to the fonts (you can also use system fonts)

    ar.setTtfFonts(
        'Calibri',
        os.path.realpath(ar.__font_dir__),
        normal=('Calibri', 'calibri.ttf'),
        bold=('CalibriBd', 'calibrib.ttf'),
        italic=('CalibriIt', 'calibrii.ttf'),
        bold_italic=('CalibriBdIt', 'calibriz.ttf'))

But you also want to have your fonts in sync with matplotlib, that's why you additionally have to:

.. code-block:: python

    fpath = os.path.join(ar.__font_dir__, 'calibri.ttf')
    font = ap.ft2font.FT2Font(fpath)
    ap.fontprop = ap.ttfFontProperty(font)

    fontprop = ap.fm.FontProperties(
        family='sans-serif',
        fname=ap.fontprop.fname,
        size=None,
        stretch=ap.fontprop.stretch,
        style=ap.fontprop.style,
        variant=ap.fontprop.variant,
        weight=ap.fontprop.weight)

    fontsize = 10
    ap.matplotlib.rcParams.update({
        'font.size': fontsize,
        'font.family': 'sans-serif'
        })

You might then additionally wan't to use the same colors, that reportlab uses:

.. code-block:: python

    from cycler import cycler

    plotColorDict = dict(
        royalblue='#4169E1',
        tomato='#FF6347',
        gold='#FFD700',
        mediumturquoise='#48D1CC',
        mediumorchid='#BA55D3',
        yellowgreen='#9ACD32',
        burlywood='#DEB887',
        darkslategray='#2F4F4F',
        orange='#FFA500',
        silver='#C0C0C0')

    plotColorNames = list(plotColorDict.keys())
    plotColors = list(plotColorDict.values())

    ap.plt.rc('axes', prop_cycle=(cycler('color', plotColors)))

