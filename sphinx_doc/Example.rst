Example
=======

I let the example in one piece, there are three examples, that will be compiled to one pdf-file:

.. code-block:: python

    import os
    from cycler import cycler

    from autobasedoc import ar
    from autobasedoc import ap

    ar.setTtfFonts(
        'Calibri',
        os.path.realpath(ar.__font_dir__),
        normal=('Calibri', 'calibri.ttf'),
        bold=('CalibriBd', 'calibrib.ttf'),
        italic=('CalibriIt', 'calibrii.ttf'),
        bold_italic=('CalibriBdIt', 'calibriz.ttf'))

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

    styles = ar.Styles()
    styles.registerStyles()

    outname = os.path.join(os.path.dirname(__file__), "MinimalExample.pdf")
    # from django.http import HttpResponse
    # outname = HttpResponse(mimetype='application/pdf')
    # outname['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    doc = ar.AutoDocTemplate(outname,onFirstPage=ar.drawLaterPage,onLaterPages=ar.drawLaterPage,onLaterSPages=ar.drawLaterPage,
                            leftMargin=0.5*ar.cm, rightMargin=0.5*ar.cm, topMargin=0.5*ar.cm, bottomMargin=0.5*ar.cm)

    content = []

    #add title
    para = ar.Paragraph(u"Minimal Example Title", styles.title)
    content.append(para)
    content.append(ar.PageBreak())

    # Create Table Of Contents. Override the level styles (optional)
    # and add the object to the story
    toc = ar.doTabelOfContents()
    content.append(ar.Paragraph(u"Inhaltsverzeichnis", styles.h1))
    content.append(toc)


    ## Example 1 adding a table
    ##############################################
    content.append(ar.PageBreak())
    ar.addHeading("A Table", styles.h1, content)

    para = ar.Paragraph(u"My Text that I can write here or take it from somewhere like shown in the next paragraph.", styles.normal)
    content.append(para)

    content.append(ar.Paragraph("Table is here.",styles.caption))

    data = [(1,2,3,4), (5,6,6,8)]

    content.append(ar.Table(data, style=None, spaceBefore=10))

    ## Example 2 adding matplotlib plot
    ##############################################
    content.append(ar.PageBreak())
    ar.addHeading("A simple Image", styles.h1, content)
    content.append(ar.Paragraph("Pictures are to be placed here.",styles.normal))

    title = "My simple plot"

    @ap.autoPdfImg
    def my_plot1(canvaswidth=5): #[inch]
        fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
        fig.suptitle(title, fontproperties=fontprop)
        x=[1,2,3,4,5,6,7,8]
        y=[1,6,8,3,9,3,4,2]
        ax.plot(x,y,label="legendlabel")
        nrow, ncol = 1, 1
        handles, labels = ax.get_legend_handles_labels()
        
        leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))
        
        ax.legend(handles, labels, #labels = tuple(bar_names)
                ncol=ncol, mode=None,
                borderaxespad=0.,
                loc='best',        # the location of the legend handles
                handleheight=None,   # the height of the legend handles
                #fontsize=9,         # prop beats fontsize
                markerscale=None,
                #frameon=False,
                prop=fontprop,
                fancybox=True
                )
        
        return fig

    content.append(my_plot1())
    para = ar.Paragraph(" ".join((u"Fig.",str(doc.figcounter()),title)), styles.caption)
    content.append(para)

    ## Example 3 adding matplotlib plot and legend
    ##############################################
    content.append(ar.PageBreak())
    ar.addHeading("An Image with Legend", styles.h1, content)
    content.append(ar.Paragraph("Pictures are to be placed here.",styles.normal))

    title = "My plot with a separate legend"

    @ap.autoPdfImage
    def my_plot2(canvaswidth=5): #[inch]
        fig, ax = ap.plt.subplots(figsize=(canvaswidth,canvaswidth))
        fig.suptitle(title,fontproperties=fontprop)
        x=[1,2,3,4,5,6,7,8]
        y=[1,6,8,3,9,3,4,2]
        ax.plot(x,y,label="legendlabel")
        nrow, ncol = 1, 1
        handles, labels = ax.get_legend_handles_labels()
        
        leg_fig = ap.plt.figure(figsize=(canvaswidth, 0.2*nrow))
        
        leg = leg_fig.legend(handles, labels, #labels = tuple(bar_names)
                ncol=ncol, 
                mode=None,
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

    img, leg = my_plot2()

    content.append(leg)
    content.append(img)
    para = ar.Paragraph(" ".join((u"Fig.",str(doc.figcounter()),title)), styles.caption)
    content.append(para)

    doc.multiBuild(content)
