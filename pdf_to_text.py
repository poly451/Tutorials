from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import os, sys
# -------------
import utils


def pdf_to_string(input_path, output_path):
    # https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
    if len(input_path) == 0 or len(output_path) == 0:
        raise ValueError("Error! At least one filepath is EMPTY!!")
    # ----
    output_string = StringIO()
    with open(input_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        text = output_string.getvalue()
    with open(output_path, "w") as f:
        f.write(text)


def main(base_dir, output_base_dir):
    please_quit = 0
    mylist = []
    for root, dirs, files in os.walk(base_dir):
        temp_root = root.replace(base_dir, output_base_dir)
        if not os.path.exists(temp_root):
            os.mkdir(temp_root)
        for file in files:
            if file.lower().find(".pdf") == -1:
                continue
            input_temp = os.path.join(root, file)
            output_temp = input_temp.replace(base_dir, output_base_dir)
            output_temp = output_temp.replace(".pdf", ".txt")
            if input_temp.find("Non-English - LT") == -1:
                # If the text file already exists, don't convert it again!
                if os.path.exists(output_temp):
                    continue
                print("Converting {}, ({})".format(file, len(mylist)))
                # ----
                please_quit += 1
                pdf_to_string(input_temp, output_temp)
                mylist.append([input_temp, output_temp])
                if please_quit > 30: return mylist

if __name__ == "__main__":
    input_directory = "/Volumes/LaCie/Multimedia Archive/Carl G. Jung"
    output_directory = "/Users/BigBlue/Documents/Programming/Python/data/texts/carl_jung_exp"
    main(input_directory, output_directory)