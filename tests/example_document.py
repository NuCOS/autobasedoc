try:
    import autobasedoc

except:
    import os, sys
    folder = "../../autobasedoc/"
    __root__ = os.path.dirname(__file__)

    importpath = os.path.realpath(os.path.join(__root__, folder))
    sys.path.append(importpath)



import copy
from flowables import create_figure, create_table, create_vertical_spacer
from flowables import create_header, create_footer, create_image
import flowables
from document import Document, ar
import simplejson as json


LOGO = "grafics/GA.svg"
USER = "grafics/Benutzer.svg"
CAL =  "grafics/Kalender.svg"
FN = "grafics/Dateiname.svg"


if __name__ == "__main__":
    ##############################
    # PORTRAIT DOCUMENT
    doc = Document(orientation="portrait")
    footerText = [["left", "left middle", "right middle", "right"]]
    rightHeaderLines = [["top line"], ["middle line"], ["bottom line"]]

    headerText = [["", "MAIN TITLE", ""]]
    header = create_header(headerText, rightHeaderLines, LOGO)
    footer = create_footer(footerText, [USER, CAL, "", FN])
                
    doc.add_footer(footer)
    doc.add_header(header)
    spacer = create_vertical_spacer(4.8)
    # table
    titleTableText = [["Title", "Title"],
                      ["Subtitle", "Subtitle"],
                      ["Datum", "Datum"]]
    titleTableData = {
            "body": titleTableText,
            "hTableAlignment": "CENTER",
            "colWidths": [8, 8],
            "fontsize": 15,
    }
    table_title = create_table(**titleTableData)
    # create a figure
    fig, leg = create_figure(hAlign=ar.TA_CENTER)
    doc.add_page(
                    bookmark=ar.Bookmark("Main Chapter", 0),
                    framestyle="single",
                    content={"center": [spacer, table_title, fig, leg]}
                )
    # NOTE: to add a png image convert it first to a pdf with: img2pdf -o out.pdf color_logo_transparent.png 
    # if added without table the image flowable is beneath all other flowables
    # if added with table it takes space as usual
    img = create_image("grafics/out.pdf", width=10, height=10)
    # img.hAlign = ar.TA_CENTER
    imgTableContent = [[img]]
    imgTableData = {
            "body": imgTableContent,
            "hTableAlignment": "CENTER",
            "centered": [(0,0)],
            "withHLines": False

    }
    img_title = create_table(**imgTableData)
    doc.add_page(
                    bookmark=ar.Bookmark("Main Chapter", 0),
                    framestyle="single",
                    content={"center": [spacer, img_title] }
                )
    

    doc.create_pdf("TEST", "Oliver", "NuCOS", "0.0.1", filename="doc_portrait.pdf")
    ###################################################
    # PORTRAIT DOCUMENT with one and two frames
    doc = Document(orientation="landscape")

    doc.add_footer(footer)
    doc.add_header(header)

    doc.add_page(
                    bookmark=ar.Bookmark("Main Chapter", 0),
                    framestyle="single",
                    content={"center": [spacer, table_title]}
                )
    frameTableText = [["Title", "Title"],
                      ["Subtitle", "Subtitle"],
                      ["Datum", "Datum"]]
    frameTableContent = {
            "body": frameTableText,
            "hTableAlignment": "CENTER",
            "colWidths": [4, 4],
            "fontsize": 12,
    }
    # next page
    
    table_frame = create_table(**frameTableContent)
    img = create_image("grafics/out.pdf", width=4, height=4)
    # img.hAlign = ar.TA_CENTER
    imgTableContent = [[img]]
    imgTableData = {
            "body": imgTableContent,
            "hTableAlignment": ar.TA_CENTER,
            "centered": [(0,0)],
    }
    img_table = create_table(**imgTableData)
    doc.add_page(
                    bookmark=ar.Bookmark("Main Chapter", 0),
                    framestyle="double",
                    content={"left": [spacer, table_frame] , "right": [spacer, img_table]}
                )
    

    doc.create_pdf("TEST", "Oliver", "NuCOS", "0.0.1", filename="doc_landscape.pdf")
    ###################################################
    # exit()
    # auto layout production
    # read in the layout definitio
    fn_layout = "layout.json"
    with open(fn_layout, encoding='utf-8') as fh:
        data = fh.read()
    current_layout = json.loads(data)

    # read in the actual document content
    fn_document = "document_for_layout.json"
    with open(fn_document, encoding='utf-8') as fh:
        doc_data_raw = fh.read()
    
    # print(doc_data)
    # get the correct layout and all data structured
    doc_data = json.loads(doc_data_raw)
    variables_global = doc_data["vars"]
    for k, v in variables_global.items():
        doc_data_raw = doc_data_raw.replace(f"${k}", v)
    doc_data = json.loads(doc_data_raw)


    orientation = doc_data["orientation"]

    def process_frame(elements=None):
        flowables = []
        for elem_name, elem_args in elements.items():
            elem_ref = current_layout[elem_name]
            code = elem_ref["code"]
            default_args = elem_ref["arguments"].copy()
            default_args.update(elem_args)
            elements = elem_ref.get("elements")
            flow = element_as_flowable(code=code, arguments=default_args, elements=elements)
            if isinstance(flow, (list, tuple)):
                flowables.extend(list(flow))
            else:
                flowables.append(flow)
        return flowables

    def element_as_flowable(code=None, arguments=None, elements=None):
        if elements:
            # replace arguments with some elements
            sub_flows = {}
            for arg_ref, elem_name in elements.items():
                elem_args = arguments[arg_ref][elem_name]
                elem_ref = current_layout[elem_name]
                sub_code = elem_ref["code"]
                default_args = elem_ref["arguments"].copy()
                default_args.update(elem_args)
                # print(".....create sub", sub_code, default_args)
                sub_flows.update({arg_ref: element_as_flowable(code=sub_code, arguments=default_args)})
                
            method = getattr(flowables, code)
            # print(".....complete sub", code, sub_flows)
            return method(**sub_flows)
        method = getattr(flowables, code)
        # print(".....create ", code, arguments)
        flow = method(**arguments)
        
        
        return flow


    standard_header = create_header(**doc_data["standard_header"])
    standard_footer = create_footer(**doc_data["standard_footer"])
    pages = doc_data["pages"]

    doc = Document(orientation=orientation)
    doc.add_header(standard_header)
    doc.add_footer(standard_footer)

    for page in pages:
        content = {}
        # print(".....", page)
        for k, v in page.items():
            if k == "framestyle":
                continue
            elif k == "bookmark":
                elem_ref = current_layout[k]
                code = elem_ref["code"]
                bookmark = element_as_flowable(code=code, arguments=v)
            elif k == "content":
                for pos, elements in v.items():
                    content.update({pos: process_frame(elements=elements)})
            # print("\n\n\n.....update", pos, content)
        doc.add_page(framestyle=page["framestyle"], bookmark=bookmark, content=content)

    #print("...................................................\n\n")
    #print(doc)
    # exit()

    doc.create_pdf("TEST", "Oliver", "NuCOS", "0.0.1", filename="doc_auto.pdf")
