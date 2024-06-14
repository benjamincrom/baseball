import os
from multiprocessing import Pool

from pypdf import PdfWriter, PdfReader
from pypdf.generic import RectangleObject



def f(arg):
    with open(f'/Volumes/B_Crom_SSD/pdf2/{arg}.pdf', "rb") as in_f:
        input1 = PdfReader(in_f)
        output = PdfWriter()
        page = input1.get_page(0)
        x, y = page.mediabox.upper_right
        page.trimbox.lower_left = (0, y/2)
        page.trimbox.upper_right = (x, y)
        page.cropbox.lower_left = (0, y/2)
        page.cropbox.upper_right = (x, y)
        page.mediabox = RectangleObject((0, y/2, x, y))
        output.add_page(page)

        with open(f'/Volumes/B_Crom_SSD/split-pdfs/{arg}-A.pdf', "wb") as out_f:
            output.write(out_f)

        input1 = PdfReader(in_f)
        output = PdfWriter()
        page = input1.get_page(0)
        x, y = page.mediabox.upper_right
        page.trimbox.lower_left = (0, 0)
        page.trimbox.upper_right = (x, y/2)
        page.cropbox.lower_left = (0, 0)
        page.cropbox.upper_right = (x, y/2)
        page.mediabox = RectangleObject((0, 0, x, y/2))
        output.add_page(page)

        with open(f'/Volumes/B_Crom_SSD/split-pdfs/{arg}-B.pdf', "wb") as out_f:
            output.write(out_f)



if __name__ == '__main__':
    file_list = [
        f.split('.', 1)[0]
        for f in os.listdir('/Volumes/B_Crom_SSD/pdf2')
        if f[-3:] == 'pdf'
    ]

    with Pool(16) as p:
        p.map(f, file_list)
