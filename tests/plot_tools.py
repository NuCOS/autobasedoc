from svglib.svglib import svg2rlg



def importSVG(filename, scale=None, height=None, width=None):
    
    if filename:
        drawing = svg2rlg(filename)
    if scale:
        drawing.scale(scale, scale)
    # the height and width is the reserved drawing place not the size of the grafic
    if height:
        drawing.height = height
    if width:
        drawing.width = width
    return drawing



